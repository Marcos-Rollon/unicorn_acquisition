from websocket_manager import WebsocketServerManager
import asyncio
import json
from unicorn_manager import UnicornManager

def on_new_value(value):
    encoded = json.dumps(value[0].tolist())
    print(encoded)
    global server
    asyncio.create_task(server.emit("eeg_data", encoded))

def on_robot_start(sid, data):
    global device
    if data["data"] == True:
        device_list = device.get_device_list()
        if len(device_list) <= 0:
            print("No device connected")
            return
        device.connect_to_device(device_list[0])
        device.start_acquisition(on_new_value)
    elif data["data"] == False:
        device.stop_acquisition()

async def main():
    global server
    global device 
    device = UnicornManager()
    server = WebsocketServerManager(
        on_connect=lambda sid: print(f"Client connected: {sid}"),
        on_disconnect=lambda sid: print(f"Client disconnected: {sid}"),
    )
    server.add_listener("robot_start", on_robot_start)
    await server.start()
    try:
        # Keep the program running until interrupted
        while True:
            await asyncio.sleep(0)

    except KeyboardInterrupt:
        # Handle Ctrl+C interruption
        print("Server interrupted. Stopping...")
        server.stop()


if __name__ == "__main__":
    asyncio.run(main())