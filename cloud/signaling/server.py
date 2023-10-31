from aiohttp import web
import socketio


VIDEO_ROOM = 'room'
subscriber_sid = None
publisher_sid = None

CONTROLS_ROOM = 'controls'
raspcar_sid = None
controller_sid = None


sio = socketio.AsyncServer(cors_allowed_origins='*', ping_timeout=35)
app = web.Application()
sio.attach(app)

@sio.event
async def connect(sid, environ):
    print('Connected', sid)


@sio.event
def disconnect(sid):
    global subscriber_sid
    global publisher_sid

    if sid in [subscriber_sid, publisher_sid]:
        if subscriber_sid == sid:
            subscriber_sid = None
        if publisher_sid == sid:
            publisher_sid = None

        sio.leave_room(sid, VIDEO_ROOM)

    print('Disconnected', sid)


@sio.event
async def publisher(sid):
    print('publisher {}'.format(sid))

    global publisher_sid
    if not publisher_sid:
        publisher_sid = sid
        sio.enter_room(sid, VIDEO_ROOM)
        await ready_or_not_video()


@sio.event
async def subscriber(sid):
    print('subscriber {}'.format(sid))

    global subscriber_sid
    if not subscriber_sid:
        subscriber_sid = sid
        sio.enter_room(sid, VIDEO_ROOM)
        await ready_or_not_video()


async def ready_or_not_video():
    global subscriber_sid
    global publisher_sid
    if subscriber_sid and publisher_sid:
        # send ready to webrtc streamer so it will call front end peer
        await sio.emit('ready', room=VIDEO_ROOM, skip_sid=subscriber_sid)


@sio.event
async def controller(sid):
    print('controller {}'.format(sid))

    global controller_sid
    if not controller_sid:
        controller_sid = sid
        sio.enter_room(sid, CONTROLS_ROOM)
        await ready_or_not_controls()


@sio.event
async def raspcar(sid):
    print('raspcar {}'.format(sid))

    global raspcar_sid
    if not raspcar_sid:
        raspcar_sid = sid
        sio.enter_room(sid, CONTROLS_ROOM)
        await ready_or_not_controls()


async def ready_or_not_controls():
    global controller_sid
    global raspcar_sid
    if controller_sid and raspcar_sid:
        # send ready to rasp car controls peer so it will call front end peer
        await sio.emit('ready', room=CONTROLS_ROOM, skip_sid=controller_sid)


@sio.event
async def data(sid, data):
    print('Message from {}: {}'.format(sid, data))

    if sid in [subscriber_sid, publisher_sid]:
        await sio.emit('data', data, room=VIDEO_ROOM, skip_sid=sid)


if __name__ == '__main__':
    web.run_app(app, port=9999)
