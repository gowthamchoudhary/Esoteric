import asyncio
import websockets


async def main():

    async with websockets.connect(
        "ws://127.0.0.1:5000/communicate"
    ) as websocket:
        text = input("enter you message")

        print("Connected to server")

        await websocket.send(f"Hello FastAPI {text}")

        response = await websocket.recv()

        print("Server:", response)


asyncio.run(main())