import asyncio
import websockets
async def send_message(websocket,username):
	while True:
		message = await asyncio.get_event_loop().run_in_executor(None,input,username + ":")
		await websocket.send(f"{username}: {message}")

async def recieve_message(websocket):
	async for message in websocket:
		print(message)
async def chat():
	uri = "ws://localhost:8765"
	username = input("Enter your username: ")
	async with websockets.connect(uri) as websocket:
		send_task = asyncio.create_task(send_message(websocket,username))
		recieve_task = asyncio.create_task(recieve_message(websocket))
		await asyncio.gather(send_task, recieve_task)


asyncio.run(chat())
