from motor.motor_asyncio import AsyncIOMotorClient
import gridfs
import os

# Pobranie URI MongoDB z pliku .env lub użycie domyślnego
MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:secret@mongodb:27017")
DATABASE_NAME = "file_storage"

# Połączenie z bazą danych MongoDB
client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]

# Tworzymy GridFS do przechowywania plików w bazie
fs = gridfs.GridFS(db)

async def save_file_to_db(filename: str, content: bytes, content_type: str):
    """Zapisuje plik do MongoDB GridFS."""
    file_id = fs.put(content, filename=filename, content_type=content_type)
    return file_id
