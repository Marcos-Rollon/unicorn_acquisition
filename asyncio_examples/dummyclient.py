import socketio
import asyncio

# Create a Socket.IO client instance
sio = socketio.AsyncClient()

# Define event handlers
@sio.event
async def connect():
    print('Connected to the server')

@sio.event
async def disconnect():
    print('Disconnected from the server')

@sio.event
async def worker_data(data):
    print('Received worker data:', data)

async def main():
    try:
        # Connect to the server
        await sio.connect('http://127.0.0.1:8080')
        print("Connected")

        # Wait for a moment to receive any server responses
        await asyncio.sleep(5)

        # Disconnect from the server
        await sio.disconnect()
        print("Disconnected")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Run the asyncio event loop
    asyncio.run(main())