from aiohttp import web
import socketio
from socketio import ConnectionRefusedError

ROOM = 'room'

sio = socketio.AsyncServer(cors_allowed_origins='*', ping_timeout=35)
app = web.Application()
sio.attach(app)

subscriber_sid = None
publisher_sid = None


@sio.event
async def connect(sid, environ):
    print('Connected', sid)
    sio.enter_room(sid, ROOM)


@sio.event
def disconnect(sid):
    global subscriber_sid
    global publisher_sid
    if subscriber_sid == sid:
        subscriber_sid = None
    if publisher_sid == sid:
        publisher_sid = None

    sio.leave_room(sid, ROOM)
    print('Disconnected', sid)


async def ready_or_not():
    global subscriber_sid
    global publisher_sid
    if subscriber_sid and publisher_sid:
        await sio.emit('ready', room=ROOM)


@sio.event
async def publisher(sid):
    print('Message from {}: {}'.format(sid))

    global publisher_sid
    if not publisher_sid:
        publisher_sid = sid
        await ready_or_not()


@sio.event
async def subscriber(sid):
    print('Message from {}: {}'.format(sid))

    global subscriber_sid
    if not subscriber_sid:
        subscriber_sid = sid
        await ready_or_not()


@sio.event
async def data(sid, data):
    print('Message from {}: {}'.format(sid, data))
    await sio.emit('data', data, room=ROOM, skip_sid=sid)


if __name__ == '__main__':
    web.run_app(app, port=9999)
