from aiohttp import web
import socketio

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

@sio.on("message")
def cosa(sid, data):
    print(sid)

if __name__ == "__main__":
    web.run_app(app)