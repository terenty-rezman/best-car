'use strict'

function control_stream() {

    // signaling methods
    let socket = io(SIGNALING_SERVER_URL, { path: SIGNALING_SERVER_PATH, autoConnect: false });

    socket.on('connect', () => {
        socket.emit('controller');
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
    let data_channel

    let createPeerConnection = () => {
        try {
            pc = new RTCPeerConnection(PC_CONFIG);
            pc.onicecandidate = onIceCandidate;
            pc.oniceconnectionstatechange = (evt) => {
                console.log(evt);
            };

            data_channel = peerConnection.createDataChannel("controls", data_channel_options);

            data_channel.onerror = (error) => {
                console.log("Data Channel Error:", error);
            };

            data_channel.onmessage = (event) => {
                console.log("Got Data Channel Message:", event.data);
            };

            data_channel.onopen = () => {
                data_channel.send("Hello World!");
            };

            data_channel.onclose = () => {
                console.log("The Data Channel is Closed");
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
    this.send_message = (msg) => data_channel.send(msg);
    this.connect = () => socket.connect();
}
