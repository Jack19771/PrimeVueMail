from fastapi import FastAPI
from pydantic import BaseModel
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import json
import os

app = FastAPI()

# Folder na zapisane pliki
os.makedirs('messages', exist_ok=True)

# Klasa danych wejściowych dla wiadomości
class EmailMessage(BaseModel):
    recipient: str
    subject: str
    body: str
    encrypt: bool = False
    sign: bool = False

# Funkcja zapisu pliku
def save_message_to_file(message_data, filename):
    with open(filename, 'w') as f:
        json.dump(message_data, f, indent=4)
    print(f"Message saved to {filename}")

# Generowanie kluczy RSA
def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    return private_key, public_key

# Funkcja szyfrowania wiadomości
def encrypt_message(message, public_key):
    cipher_rsa = PKCS1_OAEP.new(RSA.import_key(public_key))
    encrypted_message = cipher_rsa.encrypt(message.encode('utf-8'))
    return encrypted_message

# Funkcja podpisywania wiadomości
def sign_message(message, private_key):
    private_key = RSA.import_key(private_key)
    h = SHA256.new(message.encode('utf-8'))
    signer = pkcs1_15.new(private_key)
    signature = signer.sign(h)
    return signature

# Endpoint do generowania kluczy RSA
@app.post("/generate-pgp-keys")
async def generate_pgp_keys():
    private_key, public_key = generate_rsa_keys()

    # Zapisz klucze do plików
    with open('keys/public_key.pem', 'wb') as pub_file:
        pub_file.write(public_key)
    with open('keys/private_key.pem', 'wb') as priv_file:
        priv_file.write(private_key)

    return {"publicKey": public_key.decode(), "privateKey": private_key.decode()}

# Endpoint do wysyłania wiadomości
@app.post("/send-mail")
async def send_mail(email: EmailMessage):
    try:
        # Dane wiadomości w formacie JSON
        message_data = {
            "recipient": email.recipient,
            "subject": email.subject,
            "body": email.body
        }

        # Zapisz wiadomość w pliku JSON
        filename = f"messages/{email.subject.replace(' ', '_')}_{email.recipient}.json"
        save_message_to_file(message_data, filename)

        # Jeśli szyfrowanie włączone
        if email.encrypt:
            with open('keys/public_key.pem', 'rb') as pub_file:
                public_key = pub_file.read()
            encrypted_message = encrypt_message(email.body, public_key)
            encrypted_filename = f"messages/encrypted_{email.subject.replace(' ', '_')}_{email.recipient}.bin"
            with open(encrypted_filename, 'wb') as enc_file:
                enc_file.write(encrypted_message)

        # Jeśli podpisywanie włączone
        if email.sign:
            with open('keys/private_key.pem', 'rb') as priv_file:
                private_key = priv_file.read()
            signature = sign_message(email.body, private_key)
            signature_filename = f"messages/signed_{email.subject.replace(' ', '_')}_{email.recipient}.sig"
            with open(signature_filename, 'wb') as sig_file:
                sig_file.write(signature)

        return {"message": "Email processed successfully"}

    except Exception as e:
        return {"error": str(e)}

