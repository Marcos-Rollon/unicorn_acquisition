import socketio
import eventlet

sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio)

# Dictionary to store references to the spawned greenlets
spawned_greenlets = {}

def set_interval(uid, interval_seconds):
    while True:
        eventlet.sleep(interval_seconds)
        print(uid)
        sio.emit("eeg_data", "[1,2,3,4,5,6,7,8]", to=uid)

@sio.on("data")
def on_data(sid, data):
    print("Data from ", sid)
    print(data)
    sio.emit("data", {'data': 'received'}, to=sid)

@sio.on('*')
def default_handler(event, sid, data):
    print("Data to event name ", event)
    print("From sid ", sid)
    print("With data")
    print(data)

@sio.event
def connect(sid, environ, auth):
    print('connect ', sid)
    # Start the set_interval function and store the reference to the spawned greenlet
    spawned_greenlets[sid] = eventlet.spawn(set_interval, sid, 2)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    # Kill the spawned greenlet if it exists
    if sid in spawned_greenlets:
        spawned_greenlets[sid].kill()
        del spawned_greenlets[sid]


def main():
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)

if __name__ == '__main__':
    main()