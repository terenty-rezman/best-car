
import asyncio
import socketio
import aiohttp
import random
from urllib.parse import quote_plus
import json


SIGNALING_SERVER_URL = 'http://localhost:9999'
WEBRTC_STREAMER_URL = 'http://localhost:8000'

peer_id = None

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
    await handle_signaling_data(data)


async def handle_signaling_data(data):
    type = data["type"]
    print(type)
    if type == "offer":
        global peer_id
        peer_id = str(random.random())
        call_url = WEBRTC_STREAMER_URL + "/api/call?peerid=" + peer_id + "&url=" + quote_plus("videocap://0")
        options_str = "rtptransport=tcp&timeout=60&width=640&height=480" 
        call_url += "&options=" + quote_plus(options_str)

        print(call_url)

        async with aiohttp.ClientSession() as s:
            res = await s.post(call_url, data=json.dumps(data))
            res_json = await res.json(content_type=None)
            await sio.emit('data', res_json)
        
        async with aiohttp.ClientSession() as s:
            get_ice_candidates_url = WEBRTC_STREAMER_URL + "/api/getIceCandidate" + "?peerid=" + peer_id

            res = await s.get(get_ice_candidates_url)
            candidates = await res.json(content_type=None)

            for c in candidates:
                await sio.emit('data', {"type": 'candidate', "candidate": c})
    elif type == "answer":
        pass
    elif type == "candidate":
        add_candidate_url = WEBRTC_STREAMER_URL + "/api/addIceCandidate?peerid=" + peer_id
        async with aiohttp.ClientSession() as s:
            res = await s.post(add_candidate_url, data=json.dumps(data["candidate"]))


async def call_webrtc_streamer():
    async with aiohttp.ClientSession() as s:
        res = await s.get(WEBRTC_STREAMER_URL + "/api/getIceServers")
        ice_servers = await res.json(content_type=None);
        
        print(ice_servers)


async def main():
    await sio.connect(SIGNALING_SERVER_URL, transports=['websocket'])
    await sio.wait()


asyncio.run(main())
