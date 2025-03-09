import argparse
import logging
import asyncio
import os

from kademlia.network import Server

# Konfiguracja logowania
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

server = Server()


async def create_bootstrap_node():
    """Uruchamia bootstrap node."""
    log.info("🚀 Tworzenie pierwszego węzła Kademlia (bootstrap node)")
    await server.listen(8468,interface="0.0.0.0")
    log.info("✅ Węzeł bootstrap działa na porcie 8468")
    while True:
        await asyncio.sleep(3600)  # Utrzymanie działania


async def connect_to_bootstrap():
    """Łączy nowy węzeł z bootstrapem."""
    bootstrap_ip = os.getenv("BOOTSTRAP_IP", "127.0.0.1")
    bootstrap_port = int(os.getenv("BOOTSTRAP_PORT", "8468"))
    log.info(f"🔗 Próba połączenia z {bootstrap_ip}:{bootstrap_port}")

    await server.listen(8469,interface="0.0.0.0")
    await server.bootstrap([(bootstrap_ip, bootstrap_port)])
    log.info("✅ Połączono z siecią Kademlia")
    while True:
        await asyncio.sleep(3600)  # Utrzymanie działania


async def main():
    """Wybiera tryb działania na podstawie zmiennej środowiskowej."""
    node_type = os.getenv("NODE_TYPE", "node")  # Domyślnie "node"

    if node_type == "bootstrap":
        await create_bootstrap_node()
    else:
        await connect_to_bootstrap()


if __name__ == "__main__":
    asyncio.run(main())
