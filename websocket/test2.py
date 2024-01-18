from aiohttp import web
import socketio
import asyncio

sio = socketio.AsyncServer(cors_allowed_origins="*")
app = web.Application()
sio.attach(app)

global flag

flag = False


async def async_task():
    while flag:
        await asyncio.sleep(1)
        print(".")


@sio.on("message")
def handle_message(sid, data):
    global flag
    flag = not flag
    print("The flag is ", flag)

    # Start or stop the async_task based on the flag
    if flag:
        asyncio.ensure_future(async_task())


@sio.on('*')
async def any_event(event, sid, data):
    print("ups")


@sio.event
def connect(sid, environ, auth):
    print('connect ', sid)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == "__main__":
    asyncio.ensure_future(async_task())  # Start the async_task initially
    web.run_app(app)