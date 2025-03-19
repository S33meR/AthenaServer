import asyncio
import websockets
import logging 

#logging 

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler()
fileHandler =  logging.FileHandler(filename ="logAthenaServer",mode ="a")
sambaHandler = logging.FileHandler(filename ="/srv/samba/shared/logAthenaServer",mode ="a")
formatter = logging.Formatter(
	"%(asctime)s - %(levelname)s - %(message)s",
	datefmt = "%Y-%m-%d %H:%M",
)
consoleHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)
sambaHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)
logger.addHandler(fileHandler)
logger.addHandler(sambaHandler)

clients = set()
clients_lock = asyncio.Lock()
async def broadcast(sender,message):
	async with clients_lock:
		for client in clients:
			if client != clients:
				try:
					await client.send(f"Client {sender.remote_address}: {message}")
					logger.info(f"Message sent to {client.remote_address}")
				except websockets.exceptions.ConnectionClosed:
					logger.warning(f"Client {client.remote_address} disconnected unexpectedly.")
					

async def handleClient(websocket):

	async with clients_lock:
		clients.add(websocket)

	logger.info(f"Client connected: {websocket.remote_address}")
	logger.info(f"Total connected clients: {len(clients)}")

	try:
		async for message in websocket:
			await broadcast(websocket, message)

	except websockets.exceptions.ConnectionClosed:
		logger.info("Client disconnected")
		clients.remove(websocket)
	except Exception as e:
		logger.error(f"Unexpected error with {websocket.remote_address}: {e}")
	finally:
		async with clients_lock:
			clients.remove(websocket)
		logger.info(f"Remaining clients: {len(clients)}")
async def main():
	server = await websockets.serve(handleClient, "0.0.0.0", 8765)
	logger.info("Athena started")
	print("Athena server started on ws://localhost:8765")

	await server.wait_closed()

asyncio.run(main())

