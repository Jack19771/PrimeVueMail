import logging
import asyncio
import sys
from kademlia.network import Server

if len(sys.argv) != 5:
    print("Usage: python set.py <bootstrap node> <bootstrap port> <key> <value>")
    sys.exit(1)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

async def run():
    server = Server()
    await server.listen(8468)  # Użyj innego portu dla klienta
    bootstrap_node = (sys.argv[1], int(sys.argv[2]))
    
    try:
        await server.bootstrap([bootstrap_node])
    except Exception as e:
        print(f"Błąd bootstrapa: {e}")
        return

    print(f"Ustawiam klucz {sys.argv[3]} = {sys.argv[4]}")
    await server.set(sys.argv[3], sys.argv[4])
    server.stop()

asyncio.run(run())
