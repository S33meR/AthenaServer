import asyncio
import websockets

async def chat():
	uri = "ws://localhost:8765"
	async with websockets.connect(uri) as websocket:
		while True:
			message = input("You: ")
			await websocket.send(message)
			response = await websocket.recv()
			print(response)

asyncio.run(chat())
