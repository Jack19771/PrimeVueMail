from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
import os

# Pobranie URI MongoDB z pliku .env lub użycie domyślnego
MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:secret@mongodb:27017")
DATABASE_NAME = "file_storage"

# Połączenie z bazą danych MongoDB
client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]

# Używamy asynchronicznego GridFS
fs = AsyncIOMotorGridFSBucket(db)

async def save_file_to_db(filename: str, content: bytes, content_type: str):
    """Zapisuje plik do MongoDB GridFS."""
    from motor.motor_asyncio import AsyncIOMotorGridIn

    # Otwieramy nowy plik do zapisu
    grid_in = await fs.open_upload_stream(filename, metadata={"content_type": content_type})
    await grid_in.write(content)
    await grid_in.close()

    return grid_in._id  # Zwraca ID zapisanego pliku
