'use strict'

// Config variables: change them to point to your own servers
const SIGNALING_SERVER_URL = `https://${window.location.hostname}`;
const SIGNALING_SERVER_PATH = '/signaling-ws/socket.io'
const TURN_SERVER_URL = `${window.location.hostname}:5349`;
const TURN_SERVER_USERNAME = 'user1';
const TURN_SERVER_CREDENTIAL = 'thecar';

const PC_CONFIG = {
    iceServers: [
        {
            urls: 'turn:' + TURN_SERVER_URL + '?transport=tcp',
            username: TURN_SERVER_USERNAME,
            credential: TURN_SERVER_CREDENTIAL
        },
        {
            urls: 'turn:' + TURN_SERVER_URL + '?transport=udp',
            username: TURN_SERVER_USERNAME,
            credential: TURN_SERVER_CREDENTIAL
        }
    ]
};
