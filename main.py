from fastapi import FastAPI
from pydantic import BaseModel
import pgpy  # Biblioteka do obsługi PGP

app = FastAPI()

class PGPRequest(BaseModel):
    rank: str
    lastName: str
    firstName: str
    militaryUnit: str

@app.post("/generate-pgp-keys")

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pgpy  # Biblioteka do obsługi PGP

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

@app.post("/generate-pgp-keys")
async def generate_pgp_keys(request: PGPRequest):
    try:
        # Tworzymy pełne dane na podstawie przekazanych informacji
        input_data = f"{request.firstName} {request.lastName} - {request.rank} ({request.militaryUnit})"
        
        # Generowanie pary kluczy PGP
        key = pgpy.PGPKey.new(pubalg=pgpy.constants.PublicKeyAlgorithm.RSAEncryptOrSign, size=2048)
        
        # Tworzymy klucz publiczny i prywatny
        public_key = key.pubkey
        private_key = key

        # Zwracamy wygenerowane klucze (publiczny i prywatny) w formacie ASCII
        return {
            "publicKey": str(public_key),
            "privateKey": str(private_key)
        }
    
    except Exception as e:
        return {"error": str(e)}

async def generate_pgp_keys(request: PGPRequest):
    try:
        # Tworzymy pełne dane na podstawie przekazanych informacji
        input_data = f"{request.firstName} {request.lastName} - {request.rank} ({request.militaryUnit})"
        
        # Generowanie pary kluczy PGP
        key = pgpy.PGPKey.new(pubalg=pgpy.constants.PublicKeyAlgorithm.RSAEncryptOrSign, size=2048)
        
        # Tworzymy klucz publiczny i prywatny
        public_key = key.pubkey
        private_key = key

        # Zwracamy wygenerowane klucze (publiczny i prywatny) w formacie ASCII
        return {
            "publicKey": str(public_key),
            "privateKey": str(private_key)
        }
    
    except Exception as e:
        return {"error": str(e)}
