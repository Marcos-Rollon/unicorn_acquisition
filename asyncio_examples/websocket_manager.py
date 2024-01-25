from typing import Callable, Dict, Any, Optional
import socketio
import asyncio
from aiohttp import web


class WebsocketServerManager:
    """Manages a SOCKET.IO websocket server, event listening and data sending/receiving"""
    def __init__(self, 
                on_connect: Callable[[str], None],
                on_disconnect : Callable[[str], None],
                ) -> None:
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect
        self._sio : Optional[socketio.Server] = None
        self._app : Optional[socketio.WSGIApp] = None
        self._server: Optional[web.Application] = None
    
    def emit(self, event : str, data : Any, sid : Optional[str]):
        self._sio.emit(event, data, sid)
    
    def add_event(self, event: str, callback: Callable[[str, Any], None]):
        self._sio.on(event, callback)

    # async def close(self):
    #     if self._sio is not None:
    #         await self._sio.stop()
    #     if self._app is not None:
    #         await self._app.shutdown()
    #     if self._server is not None:
    #         await self._server.shutdown()
    #     if self._sio is not None and self._app is not None and self._server is not None:
    #         await self._server.wait_closed()
    #         await self._app.cleanup()

    # def stop(self):
    #     self.close()

    async def init(self, host : str = "", port : int = 8000, cors_allowed_origins : str = "*"):
        """Initializes the server with a given IP"""
        if self._sio is not None or self._app is not None or self._server is not None:
            return
        self._sio = socketio.AsyncServer(cors_allowed_origins = cors_allowed_origins)
        self._app = web.Application()
        self._sio.attach(self._app)
        @self._sio.event
        def connect(sid, environ, auth):
            if self.on_connect is not None:
                self.on_connect(sid)
        @self._sio.event
        def disconnect(sid):
            if self.on_disconnect is not None:
                self.on_disconnect(sid)

        print("Websocket server started in ", host, port)
        #Starts the server
        try:
            self._server = web.Server(self._app)
            await web.run_app(self._app, host=host, port=port)
            
        except Exception as e:
            print(f"Failed to start the server: {e}")

        

        