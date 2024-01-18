import socketio
import time

# Define the Socket.IO client
sio = socketio.Client()

# Define event handlers
@sio.event
def connect():
    print("Connected to the server")

@sio.event
def disconnect():
    print("Disconnected from the server")

@sio.event
def custom_event(data):
    print(f"Received custom event: {data}")

# Connect to the server
sio.connect('http://localhost:8000')  # Replace with your server URL

# Wait for a moment to ensure connection
time.sleep(1)

# Emit a custom event to the server
sio.emit('close', {'message': 'Hello from the client!'})

# Wait for a moment before disconnecting
time.sleep(1)

# Disconnect from the server
sio.disconnect()
