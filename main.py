from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Crypto.PublicKey import RSA
import os
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import json
import base64
import subprocess
from kademlia.network import Server
import asyncio
from routes import upload  # <-- Importujemy nasz plik `upload.py`

app = FastAPI()
app.include_router(upload.router)

# Lista aktywnych połączeń WebSocket
active_connections = []
# Globalny stan alertu
alert_state = {"alert": None}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        print("WebSocket connection accepted")
        active_connections.append(websocket)
        
        while True:
            message = await websocket.receive_text()
            try:
                data = json.loads(message)  # Parsujemy JSON
                print(f"Received message: {data}")  # Logowanie wiadomości

                # Dodaj timestamp na serwerze, jeśli go nie ma
                if "timestamp" not in data:
                    from datetime import datetime
                    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Wysyłamy wiadomość do wszystkich klientów (łącznie z nadawcą)
                for connection in active_connections:
                    await connection.send_text(json.dumps(data))  # Wysyłamy JSON
                
            except json.JSONDecodeError:
                print("Received invalid JSON message")  # Obsługa błędów JSON
            
    except WebSocketDisconnect:
        print("WebSocket disconnected")
        active_connections.remove(websocket)

@app.post("/send-alert")
async def send_alert(alert: dict):
    # Zapisz status alertu do bazy danych, pliku, lub w pamięci
    alert_status = alert.get("alert", False)
    alert_state["alert"] = alert_status  # Uaktualniamy stan alertu
    
    # Powiadom wszystkich połączonych klientów
    await notify_clients()
    
    return {"message": f"Alert status: {alert_status}"}

async def notify_clients():
    # Przesyłanie danych alertu do wszystkich połączonych klientów za pomocą SSE
    for connection in active_connections:
        try:
            # Wysłanie alertu do połączonych klientów
            if alert_state["alert"]:
                await connection.send_text(f"Alert: {alert_state['alert']}")
            else:
                await connection.send_text("Alert deactivated")
        except WebSocketDisconnect:
            active_connections.remove(connection)

@app.get("/get-alert-status")
async def get_alert_status():
    # Zwróć aktualny status alertu
    return {"alert": alert_state["alert"]}

def call_set_script(bootstrap_node, bootstrap_port, key, value):
    # Używamy subprocess do wywołania set.py z odpowiednimi argumentami
    try:
        subprocess.run(['python', 'set.py', bootstrap_node, str(bootstrap_port), key, value], check=True)
        print("Dane zostały pomyślnie wstawione do Kademlia.")
    except subprocess.CalledProcessError as e:
        print(f"Błąd podczas wywoływania set.py: {e}")

# Dodanie CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Możesz ograniczyć do konkretnych źródeł, np. ["http://localhost:8080"]
    allow_credentials=True,
    allow_methods=["*"],  # Możesz ograniczyć do określonych metod
    allow_headers=["*"],  # Możesz ograniczyć do określonych nagłówków
)

class PGPRequest(BaseModel):
    rank: str
    lastName: str
    firstName: str
    militaryUnit: str

# Funkcja zapisu kluczy do plików
def save_key_to_file(key, filename):
    # Tworzymy folder "keys" w bieżącym katalogu, jeśli nie istnieje
    if not os.path.exists('keys'):
        os.makedirs('keys')
    
    file_path = os.path.join('keys', filename)
    with open(file_path, 'w') as f:
        f.write(key)
    print(f"Klucz zapisany w pliku: {file_path}")

@app.post("/generate-pgp-keys")
async def generate_pgp_keys(request: PGPRequest):
    try:
        # Tworzymy pełne dane na podstawie przekazanych informacji
        input_data = f"{request.firstName} {request.lastName} - {request.rank} ({request.militaryUnit})"
        
        # Debug: Logujemy dane wejściowe
        print(f"Generowanie kluczy dla: {input_data}")

        # Generowanie klucza RSA
        print("Rozpoczynanie generowania kluczy RSA...")

        # Tworzymy parę kluczy RSA
        key = RSA.generate(2048)  # 2048-bitowy klucz RSA
        
        # Klucz publiczny
        public_key = key.publickey().export_key().decode('utf-8')

        # Klucz prywatny
        private_key = key.export_key().decode('utf-8')

        # Zapisujemy klucze do plików
        save_key_to_file(public_key, 'public_key.pem')
        save_key_to_file(private_key, 'private_key.pem')

        # Debug: Logujemy wygenerowane klucze
        print("Klucze RSA wygenerowane i zapisane.")

        return {
            "publicKey": public_key,
            "privateKey": private_key
        }

    except Exception as e:
        return {"error": str(e)}

os.makedirs('messages', exist_ok=True)
os.makedirs('keys', exist_ok=True)

class EmailMessage(BaseModel):
    recipient: str
    subject: str
    body: str

def save_message_to_file(message_data, filename):
    with open(filename, 'w') as f:
        json.dump(message_data, f, indent=4)
    print(f"Message saved to {filename}")

# Funkcja do szyfrowania wiadomości
def encrypt_message(message, public_key):
    cipher_rsa = PKCS1_OAEP.new(RSA.import_key(public_key))
    encrypted_message = cipher_rsa.encrypt(message.encode('utf-8'))
    
    # Kodowanie zaszyfrowanej wiadomości w Base64
    encrypted_message_base64 = base64.b64encode(encrypted_message).decode('utf-8')
    
    return encrypted_message_base64

# Funkcja do podpisywania wiadomości
def sign_message(message, private_key):
    private_key = RSA.import_key(private_key)
    h = SHA256.new(message.encode('utf-8'))
    signer = pkcs1_15.new(private_key)
    signature = signer.sign(h)
    return signature

@app.post("/send-mail")
async def send_mail(email: EmailMessage):
    try:
        # Przygotowanie danych wiadomości
        message_data = {
            "recipient": email.recipient,
            "subject": email.subject,
            "body": email.body,
        }
        filename = f"messages/{email.subject.replace(' ', '_')}_{email.recipient}.json"
        save_message_to_file(message_data, filename)

        # Wczytanie klucza publicznego i szyfrowanie wiadomości
        with open('keys/public_key.pem', 'rb') as pub_file:
            public_key = pub_file.read()
        encrypted_message = encrypt_message(email.body, public_key)
        encrypted_filename = f"messages/encrypted_{email.subject.replace(' ', '_')}_{email.recipient}.txt"  # Używamy .txt dla ASCII
        with open(encrypted_filename, 'w') as enc_file:
            enc_file.write(encrypted_message)  # Zapisujemy zaszyfrowaną wiadomość w Base64 jako tekst
            call_set_script('51.12.244.193', 8468, 'email', 'Jacek')
            #
        # Wczytanie klucza prywatnego i podpisywanie wiadomości
        with open('keys/private_key.pem', 'rb') as priv_file:
            private_key = priv_file.read()
        signature = sign_message(email.body, private_key)
        signature_filename = f"messages/signed_{email.subject.replace(' ', '_')}_{email.recipient}.sig"
        with open(signature_filename, 'wb') as sig_file:
            sig_file.write(signature)  # Zapisanie podpisu

        return {"message": "Email processed successfully"}
    except Exception as e:
        return {"error": str(e)}
