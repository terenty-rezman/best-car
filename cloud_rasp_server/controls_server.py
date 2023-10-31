import asyncio
import socketio
import aiohttp
from aiortc import RTCIceCandidate, RTCPeerConnection, RTCSessionDescription
import json

from settings import *


pc = None
early_candidates = []
remote_descr_set = False

# asyncio
sio = socketio.AsyncClient()


@sio.event
async def connect():
    print("I'm connected!")
    await sio.emit('raspcar')


@sio.event
def connect_error(data):
    print("The connection failed!")


@sio.event
def disconnect():
    print("I'm disconnected!")


@sio.event
async def ready():
    print('ready')
    await create_peer()


@sio.event
async def data(data):
    await handle_signaling_data(data)


async def add_ice_candidate(c):
    print('add remote ice candidate:', c)
    pc.addIceCandidate(c)


async def handle_signaling_data(data):
    type = data["type"]
    print("received event:", type)

    global pc
    global remote_descr_set
    global early_candidates

    if type == "answer":
        await pc.setRemoteDescription(data)
        remote_descr_set = True

        for c in early_candidates:
            await add_ice_candidate(c)
        early_candidates = []
    elif type == "candidate":
        if remote_descr_set:
            await add_ice_candidate(data["candidate"])
        else:
            print("early candidate")
            early_candidates.append(data["candidate"])


async def create_peer():
    global pc
    global early_candidates
    global remote_descr_set
    early_candidates = []
    remote_descr_set = False

    pc = RTCPeerConnection()
    channel = pc.createDataChannel("controls")

    @channel.on("open")
    def on_open():
        print("channel opened")

    @channel.on("message")
    def on_message(message):
        print(channel, "<", message) 
    
    await pc.setLocalDescription(await pc.createOffer())
    await sio.emit('data', pc.localDescription)


async def main():
    while(True):
        try:
            await sio.connect(SIGNALING_SERVER_URL, socketio_path='signaling-ws/socket.io')
            break
        except socketio.exceptions.ConnectionError as e:
            print(e)
            await asyncio.sleep(2)

    print("connected to signaling server")
    await sio.wait()


asyncio.run(main())
