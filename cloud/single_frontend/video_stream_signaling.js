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

function raspi_video_stream(remote_stream_element_selector) {

    // signaling methods
    let socket = io(SIGNALING_SERVER_URL, { path: SIGNALING_SERVER_PATH, autoConnect: false });

    socket.on('connect', () => {
        socket.emit('subscriber');
    });

    socket.on('data', (data) => {
        console.log('Data received: ', data);
        handleSignalingData(data);
    });

    let sendData = (data) => {
        socket.emit('data', data);
    };

    // WebRTC methods
    let pc;
    let remoteStreamElement = document.querySelector(remote_stream_element_selector || '#remoteStream');

    let createPeerConnection = () => {
        try {
            pc = new RTCPeerConnection(PC_CONFIG);
            pc.onicecandidate = onIceCandidate;
            pc.ontrack = onTrack;
            pc.oniceconnectionstatechange = (evt) => {
                console.log(evt);
            };
            console.log('PeerConnection created');
        } catch (error) {
            console.error('PeerConnection failed: ', error);
        }
    };

    let sendAnswer = () => {
        console.log('Send answer');
        pc.createAnswer()
            .then((answer) => { pc.setLocalDescription(answer); return answer; })
            .then((answer) => { sendData(answer); console.log("local description set"); })
            .catch((e) => console.log(e));
    };

    let setAndSendLocalDescription = (sessionDescription) => {
        pc.setLocalDescription(sessionDescription, () => {
            sendData(sessionDescription);
            console.log('Local description set');
        });
    };

    let onIceCandidate = (event) => {
        if (event.candidate) {
            console.log('local ICE candidate');
            sendData({
                type: 'candidate',
                candidate: event.candidate
            });
        }
    };

    let onTrack = (event) => {
        console.log('Add track');
        console.log('streams len:', event.streams.length);
        remoteStreamElement.srcObject = event.streams[0];
    };

    let handleSignalingData = (data) => {
        switch (data.type) {
            case 'offer':
                createPeerConnection();
                pc.setRemoteDescription(new RTCSessionDescription(data)).then(sendAnswer);
                break;
            case 'answer':
                pc.setRemoteDescription(new RTCSessionDescription(data));
                break;
            case 'candidate':
                console.log("remote ice candidate")
                pc.addIceCandidate(new RTCIceCandidate(data.candidate));
                break;
        }
    };

    this.socket = socket;
    this.pc = pc;
    this.connect = () => socket.connect();
}
