from fastapi import APIRouter

router = APIRouter()

from fastapi import UploadFile, File, HTTPException
import uuid
from utils.database import save_file_to_db  # Za chwilę dodamy tę funkcję

@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    allowed_types = ["application/pdf", "image/jpeg", "image/png"]
    
    # Sprawdzenie typu pliku
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Nieprawidłowy typ pliku")

    contents = await file.read()  # Odczytaj zawartość pliku
    
    # Ograniczenie rozmiaru pliku (np. max 10MB)
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Plik jest za duży")

    filename = f"{uuid.uuid4()}_{file.filename}"  # Generowanie unikalnej nazwy

    # Zapis pliku do MongoDB (GridFS)
    file_id = await save_file_to_db(filename, contents, file.content_type)

    return {"file_id": str(file_id), "filename": filename, "message": "Plik został zapisany w bazie danych"}
