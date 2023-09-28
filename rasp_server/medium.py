from flask import Flask, request
from flask_socketio import SocketIO, emit
import mimetypes

# fix for windows (otherwise module .js served as text/plain)
mimetypes.add_type('application/javascript', '.js')


class CustomFlask(Flask):
    # remove caching time for js files
    def get_send_file_max_age(self, name):
        if name.lower().endswith('.js'):
            return 0
        return Flask.get_send_file_max_age(self, name)


_app = CustomFlask(__name__,
                   static_url_path='',
                   static_folder='frontend')

_socketio = SocketIO(_app)
_update_callbacks = dict()
_values = dict()
_disconnect_callback = None


@_app.route('/')
def home():
    return _app.send_static_file('index.html')


@_socketio.on('connect')
def _on_client_connected():
    print(f'\nclient {request.sid} connected')


@_socketio.on('disconnect')
def _on_client_disconnected():
    print(f'client {request.sid} disconnected')
    if _disconnect_callback:
        _disconnect_callback(request.sid)


@_socketio.on('provide')
def _provide_value(json):
    var_name = json['name']

    value = _values.get(var_name, None)
    if value is not None:
        emit('changed', {'name': var_name, 'value': value})  # respond to one


@_socketio.on('changed')
def _on_changed(json):
    name = json['name']
    value = json['value']

    set(name, value)

    callback = _update_callbacks.get(name, None)
    if callback:
        callback(value, request.sid)


def subscribe(var_name):
    def decorator(callback):
        _update_callbacks[var_name] = callback
        return callback
    return decorator


def set(name, value):
    _values[name] = value
    _socketio.emit('changed', {'name': name, 'value': value})  # notify all


def get(name):
    return _values.get(name, None)


def on_disconnect():
    def decorator(callback):
        _disconnect_callback = callback
        return callback
    return decorator


def listen(host, port):
    print(f'server running on {host}:{port}')
    _socketio.run(_app, host=host, port=port)
