from websocket_manager import WebsocketServerManager
import asyncio

global worker_state
global worker_task
worker_task = None
worker_state = False

async def worker(callback):
    counter = 0
    while True:
        await asyncio.sleep(1)
        counter += 1
        value = f"Counter: {counter}"
        callback(value)
def start_worker(callback):
    global worker_state, worker_task
    if worker_state is False and worker_task is None:
        worker_task = asyncio.create_task(worker(callback))
        worker_state = True
    else:
        print("Trying to start the worker when is already running")
def stop_worker():
    global worker_state, worker_task
    if worker_state is True and worker_task is not None:
        worker_task.cancel()
        worker_task = None
        worker_state = False
    else:
        print("Trying to stop a task that's not running")


def on_new_value(value):
    print(f"Received value from worker: {value}")
    global server
    asyncio.create_task(server.emit("worker_data", value))

def on_event(sid, data):
    if data is True:
        print("Starting task...")
        start_worker(on_new_value)
    elif data is False:
        print("Stopping task...")
        stop_worker()
    else:
        pass


async def main():
    global server
    server = WebsocketServerManager(
        on_connect=lambda sid: print(f"Client connected: {sid}"),
        on_disconnect=lambda sid: print(f"Client disconnected: {sid}"),
    )
    server.add_listener("start_task", on_event)
    
    #server_task = asyncio.create_task(server.start(port=8080))
    #data_acquisition = asyncio.create_task(worker(on_new_value))
    await server.start()
    # await asyncio.gather(
    #     server_task,
    #     #data_acquisition,
    # )
    try:
        # Keep the program running until interrupted
        while True:
            await asyncio.sleep(0)

    except KeyboardInterrupt:
        # Handle Ctrl+C interruption
        print("Server interrupted. Stopping...")
        # Cancel the worker task before stopping the server
        #server_task.cancel()
        #data_acquisition.cancel()
        server.stop()


if __name__ == "__main__":
    asyncio.run(main())