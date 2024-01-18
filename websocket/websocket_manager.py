from typing import Callable, Dict, Any, Optional
import socketio
from aiohttp import web

class WebsocketServerManager:
    """Manages a SOCKET.IO websocket server, event listening and data sending/receiving"""
    def __init__(self, 
                on_connect: Callable[[str], None],
                on_disconnect : Callable[[str], None],
                show_logs: bool = True,
                ) -> None:
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect
        self.show_logs = show_logs
        self._listeners : Dict[str, Callable[[Any], None ]] = {} # To store every listener
        self._sio : Optional[socketio.Server] = None
        self._app : Optional[socketio.WSGIApp] = None
        self._server: Optional[web.Application] = None

    def add_listener(self, event : str, callback : Callable[[str, Any], None]):
        """Add an event listener for the event name"""
        if event in self._listeners:
            if self.show_logs:
                print("Cannot add a listener. Event listener already exits")
            return
        self._listeners[event] = callback
        if self._sio is not None:
            self._sio.on(event, lambda sid, data : callback(sid, data))

    def remove_listener(self, event):
        """Remove an event listener"""
        if event in self._listeners:
            self._sio.off(event, self._listeners[event])
            del self._listeners[event]
        
    def remove_all_listeners(self):
        """Removes all active listeners"""
        for event, callback in self._listeners.items():
            self._sio.off(event, callback)
        self._listeners.clear()
    
    def emit(self, event : str, data : Any, sid : Optional[str]):
        self._sio.emit(event, data, sid)
    
    def init(self, host : str = "", port : int = 8000, cors_allowed_origins : str = "*"):
        """Initializes the server with a given IP"""
        if self._sio != None or self._app != None or self._server != None:
            if self.show_logs:
                print("There is already a server running. Close that first before initializing")
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
        if len(self._listeners) > 0:
            # add all the listener to sio
            for event, callback in self._listeners.items():
                self._sio.on(event, lambda sid, data : callback(sid, data))
        if self.show_logs:
            print("Websocket server started in ", host, port)
        #Starts the server
        self._server = web.run_app(self._app)

    def stop(self,):
        """Stops the server and deletes all current listeners"""
        if self._sio == None or self._app == None:
            if self.show_logs:
                print("Cannot stop server. Server is not running")
            return
        self.remove_all_listeners()
        self._sio.disconnect()

        self._sio = None
        self._app = None
        self._server = None
        if self.show_logs:
            print("Server stopped. All event handlers deleted")
        

        