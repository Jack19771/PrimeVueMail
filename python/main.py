from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import json
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs('messages', exist_ok=True)
os.makedirs('keys', exist_ok=True)

class EmailMessage(BaseModel):
    recipient: str
    subject: str
    body: str
    encrypt: bool = False
    sign: bool = False

def save_message_to_file(message_data, filename):
    with open(filename, 'w') as f:
        json.dump(message_data, f, indent=4)
    print(f"Message saved to {filename}")

def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

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
        message_data = {
            "recipient": email.recipient,
            "subject": email.subject,
            "body": email.body,
        }
        filename = f"messages/{email.subject.replace(' ', '_')}_{email.recipient}.json"
        save_message_to_file(message_data, filename)

        if email.encrypt:
            with open('keys/public_key.pem', 'rb') as pub_file:
                public_key = pub_file.read()
            encrypted_message = encrypt_message(email.body, public_key)
            encrypted_filename = f"messages/encrypted_{email.subject.replace(' ', '_')}_{email.recipient}.bin"
            with open(encrypted_filename, 'wb') as enc_file:
                enc_file.write(encrypted_message)

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
