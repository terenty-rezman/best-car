
import asyncio
import socketio
import aiohttp


SIGNALING_SERVER_URL = 'http://localhost:9999'
WEBRTC_STREAMER_URL = 'http://localhost:8000'


# asyncio
sio = socketio.AsyncClient()


@sio.event
def connect():
    print("I'm connected!")


@sio.event
def connect_error(data):
    print("The connection failed!")


@sio.event
def disconnect():
    print("I'm disconnected!")


@sio.event
async def ready():
    print('ready')
    await call_webrtc_streamer()


@sio.event
async def data(data):
    print(data)


async def handle_signaling_data(data):
    type = data["type"]
    if type == "offer":
        pass
    elif type == "answer":
        pass
    elif type == "candidate":
        pass


async def call_webrtc_streamer():
    async with aiohttp.ClientSession() as s:
        res = await s.get(WEBRTC_STREAMER_URL + "/api/getIceServers")
        ice_servers = await res.json(content_type=None);
        
        print(ice_servers)


async def main():
    await sio.connect(SIGNALING_SERVER_URL, transports=['websocket'])
    await sio.wait()


asyncio.run(main())
