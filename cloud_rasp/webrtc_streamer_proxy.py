
import asyncio
import socketio
import aiohttp
import random
from urllib.parse import quote_plus
import json


SIGNALING_SERVER_URL = 'https://2089517-cn34567.twc1.net'
WEBRTC_STREAMER_URL = 'http://localhost:8000'

peer_id = None
early_candidates = []
peers_ready = False

# asyncio
sio = socketio.AsyncClient()


@sio.event
async def connect():
    print("I'm connected!")
    await sio.emit('publisher')


@sio.event
def connect_error(data):
    print("The connection failed!")


@sio.event
def disconnect():
    print("I'm disconnected!")


@sio.event
async def ready():
    print('ready')
    await init_webrtcstreamer()


@sio.event
async def data(data):
    await handle_signaling_data(data)


async def webrtcstreamer_add_ice_candidate(c):
    print('send candidate:', c)
    add_candidate_url = WEBRTC_STREAMER_URL + "/api/addIceCandidate?peerid=" + peer_id
    async with aiohttp.ClientSession() as s:
        res = await s.post(add_candidate_url, data=json.dumps(c))


async def webrtc_streamer_get_ice_candidates_multiple():
    async with aiohttp.ClientSession() as s:
        # poll candidates multiple times
        for i in range(3):
            get_ice_candidates_url = WEBRTC_STREAMER_URL + "/api/getIceCandidate" + "?peerid=" + peer_id

            res = await s.get(get_ice_candidates_url)
            candidates = await res.json(content_type=None)

            for c in candidates:
                print("local candidate:", c)
                await sio.emit('data', {"type": 'candidate', "candidate": c})

            if i < 2:
                await asyncio.sleep(1)



async def handle_signaling_data(data):
    type = data["type"]
    print("received event:", type)

    global peers_ready
    global early_candidates

    if type == "offer":
        global peer_id
        peer_id = str(random.random())
        call_url = WEBRTC_STREAMER_URL + "/api/call?peerid=" + peer_id + "&url=" + quote_plus("videocap://0")
        options_str = "rtptransport=tcp&timeout=60&width=1280&height=720&fps=30" 
        call_url += "&options=" + quote_plus(options_str)

        print(call_url)

        async with aiohttp.ClientSession() as s:
            res = await s.post(call_url, data=json.dumps(data))
            streamer_descr = await res.json(content_type=None)
            await sio.emit('data', streamer_descr)

        peers_ready = True

        print("sleeping a bit to let streamer collect its ice candidates...")

        for c in early_candidates:
            await webrtcstreamer_add_ice_candidate(c)
        early_candidates = []

        await webrtc_streamer_get_ice_candidates_multiple()
    elif type == "answer":
        raise Exception("answer?")
    elif type == "candidate":
        if peers_ready:
            await webrtcstreamer_add_ice_candidate(data["candidate"])
        else:
            early_candidates.append(data["candidate"])


async def init_webrtcstreamer():
        async with aiohttp.ClientSession() as s:
            res = await s.get(WEBRTC_STREAMER_URL + "/api/getIceServers")
            ice_servers = await res.json(content_type=None);

            print(ice_servers)

        global early_candidates
        global peers_ready
        early_candidates = []
        peers_ready = False


async def main():
    await sio.connect(SIGNALING_SERVER_URL, socketio_path='signaling-ws/socket.io')
    print("connected to signaling server")
    await sio.wait()


asyncio.run(main())
