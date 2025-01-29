from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Crypto.PublicKey import RSA
import os
from pydantic import BaseModel
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import json


app = FastAPI()

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

def encrypt_message(message, public_key):
    cipher_rsa = PKCS1_OAEP.new(RSA.import_key(public_key))
    encrypted_message = cipher_rsa.encrypt(message.encode('utf-8'))
    return encrypted_message

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
        encrypted_filename = f"messages/encrypted_{email.subject.replace(' ', '_')}_{email.recipient}.bin"
        with open(encrypted_filename, 'wb') as enc_file:
            enc_file.write(encrypted_message)  # Zapisanie zaszyfrowanej wiadomości

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


