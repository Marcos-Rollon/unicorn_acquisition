from websoket_manager import WebsocketServerManager


def handle_close_event(sid, data):
    print("close event")
    print(data)

websocket_manager = WebsocketServerManager(
    lambda sid : print("Connected ", sid), 
    lambda sid : print("Disconnected ", sid)
    )

websocket_manager.init("", 8000)

websocket_manager.add_listener("close", handle_close_event)

