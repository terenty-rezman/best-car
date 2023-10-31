'use strict'

function raspi_video_stream(remote_stream_element_selector) {
    remote_stream_element_selector = remote_stream_element_selector || '#remoteStream'

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
    let remoteStreamElement = document.querySelector(remote_stream_element_selector);

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
            case 'candidate':
                console.log("remote ice candidate")
                pc.addIceCandidate(new RTCIceCandidate(data.candidate));
                break;
        }
    };

    this.socket = socket;
    this.connect = () => socket.connect();
}
