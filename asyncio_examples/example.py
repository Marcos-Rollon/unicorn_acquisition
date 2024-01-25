import asyncio
import socketio
import asyncio
from aiohttp import web

async def worker(callback):
    while True:
        # Simulate some work
        await asyncio.sleep(1)
        # Produce a value and notify the main loop
        value = "Some data from the worker"
        await callback(value)

app = web.Application()
sio = socketio.AsyncServer(cors_allowed_origins="*")
sio.attach(app)

# Callback function to send data to connected clients
async def send_data_to_clients(value):
    # Broadcasting the data to all connected clients
    print("Broadcasting: ", value)
    await sio.emit("worker_data", {"data": value})


@sio.event
def connect(sid, environ, auth):
    print("Connected :",sid)
@sio.event
def disconnect(sid):
    print("Disconnected :", sid)
@sio.event
def start_task(sid):
    print("Starting task...")

@sio.event
def stop_task(sid):
    print("Stop task...")

async def main():
    # Use AppRunner to run the web application
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Start the web server using TCPSite and AppRunner
    site = web.TCPSite(runner, '', 8080)
    await site.start()

    # Start the worker
    worker_task = asyncio.create_task(worker(lambda value: send_data_to_clients(value)))

    # Wait for both tasks to complete
    await asyncio.gather(worker_task)


if __name__ == "__main__":
    asyncio.run(main())