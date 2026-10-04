import asyncio
import websockets


async def send_message(websocket):
    while True:
        message = await asyncio.to_thread(input, "You: ")
        await websocket.send(message)


async def receive_message(websocket):
    while True:
        message = await websocket.recv()
        print(f"\nOther: {message}")


async def main():

    client_id = input("Enter your ID: ")
    recv_id = input("Enter the receiver ID: ")

    async with websockets.connect(
        f"ws://127.0.0.1:5000/communicate/{client_id}/{recv_id}"
    ) as websocket:

        await asyncio.gather(
            send_message(websocket),
            receive_message(websocket)
        )


asyncio.run(main())