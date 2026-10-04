import asyncio
import websockets



async def send_message(websocket):
    while True:
        message = await asyncio.to_thread(input,"you")
        await websocket.send(message)
async def recieve_message(websocket):
    while True:
        message = await websocket.recv()
        print(f"\nother:{message}")
async def main():
    async with websockets.connect(
        "ws://127.0.0.1:5000/communicate"
    ) as websocket:
            await asyncio.gather(
                 send_message(websocket),
                 recieve_message(websocket)

            )
asyncio.run(main())