import socketio
import time

# Create a Socket.IO client instance
sio = socketio.Client()

# Define event handlers
@sio.on('connect')
def on_connect():
    print('Connected to the server')

@sio.on('disconnect')
def on_disconnect():
    print('Disconnected from the server')

@sio.on('server_message')
def on_server_message(data):
    print('Received message from server:', data)

# Connect to the server
sio.connect('http://0.0.0.0:8080')  

# Wait for a moment to ensure connection
time.sleep(1)

print("sending")
sio.emit('message', {'message': 'Hello from the client!'})
time.sleep(10)
print("sending 2")
sio.emit('message', {'message': 'Hello from the client!'})


sio.disconnect()