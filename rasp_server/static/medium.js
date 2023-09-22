'use strict'

export class Medium {
    constructor(address_port_str) {
        this.socket = io.connect(address_port_str);
        this.subscriptions = new Map();

        this.socket.on('reconnect', this._on_reconnect.bind(this));
        this.socket.on('changed', this._on_value_changed.bind(this));
    }

    _on_reconnect() {
        this.subscriptions.forEach((callback, name) => {
            this._request_value(name);
        });
    }

    _on_value_changed(json) {
        const name = json.name;
        const value = json.value;
        let callback = this.subscriptions.get(name);

        if (callback)
            callback(value);
    }

    _request_value(var_name) {
        this.socket.emit('provide', { name: var_name });
    }

    subscribe(var_name, callback) {
        this.subscriptions.set(var_name, callback);
        this._request_value(var_name);
    }

    set(var_name, value) {
        this.socket.emit('changed', { name: var_name, value: value });
    }
}