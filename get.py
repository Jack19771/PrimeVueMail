import logging
import asyncio
import sys
from kademlia.network import Server

if len(sys.argv) != 4:
    print("Usage: python get.py <bootstrap node> <bootstrap port> <key>")
    sys.exit(1)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

async def run():
    server = Server()
    await server.listen(8470)  # Możesz zmienić port, jeśli 8469 jest zajęty
    bootstrap_node = (sys.argv[1], int(sys.argv[2]))
    await server.bootstrap([bootstrap_node])
    
    try:
        value = await server.get(sys.argv[3])
        print(f"🔍 Wartość dla klucza '{sys.argv[3]}': {value}")
    except Exception as e:
        print(f"❌ Błąd podczas pobierania: {e}")

    server.stop()

asyncio.run(run())
