from websocket_manager import WebsocketServerManager
 

async def some_task():
    while True:
        await asyncio.sleep(2)
        print(".")


async def main():
    server = WebsocketServerManager(
    lambda sid : print("Connected ", sid), 
    lambda sid : print("Disconnected ", sid)
    )
    server.add_listener("example", handle_example )
    server.init()

def handle_example(sid, data):
    print(sid)

if __name__ == "__main__":
    asyncio.run(main())