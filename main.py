from websocket_manager import WebsocketServerManager
import asyncio
from dummy_worker import Worker

def on_new_value(value):
    print(f"Received value from worker: {value}")
    global server
    asyncio.create_task(server.emit("worker_data", value))

def on_event(sid, data):
    global worker 
    if data is True:
        print("Starting task...")
        worker.start_acquisition(on_new_value)
    elif data is False:
        print("Stopping task...")
        worker.stop_acquisition()
    else:
        pass

async def main():
    global server
    global worker 
    worker = Worker()
    server = WebsocketServerManager(
        on_connect=lambda sid: print(f"Client connected: {sid}"),
        on_disconnect=lambda sid: print(f"Client disconnected: {sid}"),
    )
    server.add_listener("start_task", on_event)
    await server.start()
    try:
        # Keep the program running until interrupted
        while True:
            await asyncio.sleep(0)

    except KeyboardInterrupt:
        # Handle Ctrl+C interruption
        print("Server interrupted. Stopping...")
        server.stop()


if __name__ == "__main__":
    asyncio.run(main())