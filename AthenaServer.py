import asyncio
import websockets
import logging 

#logging 

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler()
fileHandler =  logging.FileHandler(filename = "/srv/samba/shared/logAthenaServer",mode ="a")

formatter = logging.Formatter(
	"%(asctime)s - %(levelname)s - %(message)s",
	datefmt = "%Y-%m-%d %H:%M",
)
consoleHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)

logger.addHandler(consoleHandler)
logger.addHandler(fileHandler)

clients = set()

async def handleClient(websocket, path):
	async with asyncio.Lock():
		clients.add(websocket)

	logger.info(f"Client connected: {websocket.remote_address}")
	logger.info(f"Total connected clients: {len(clients)}")

	try:
		async for message in websocket:
			logging.info(f"Recieved from {websocket.remote_address}: {message}")
			for client in clients:
				print("Connected to Athena")
				if client !=websocket:
					await client.send(f"Client: {message}")






	except websockets.exceptions.ConnectionClosed:
		print("Client disconnected")
		clients.remove(websocket)
async def main():
	server = await websockets.serve(handleClient, "0.0.0.0", 8765)
	logger.info("Athena started")
	print("Athena server started on ws://localhost:8765")

	await server.wait_closed()

asyncio.run(main())

