'use strict'
import { Medium } from './medium.js'

const medium = new Medium('http://' + document.domain + ':' + location.port);

const slider = document.getElementById('control_speed');
const display1 = document.getElementById('display1');
const display2 = document.getElementById('display2');
const fullscreen_btn = document.getElementById('fullscreen_btn');
const reload_btn = document.getElementById('reload_btn');

const camera = document.getElementById('camera');

if (!window.use_webrtc) {
    camera.src = window.location.protocol + "//" + window.location.hostname + ":5050/video_feed"
}

// slider.addEventListener('input', e => medium.set('speed', Number(slider.value)))

fullscreen_btn.addEventListener('click', e => toggleFullScreen())
reload_btn.addEventListener('click', e => location.reload())

medium.subscribe('speed', (value) => {
    // slider.value = value;
    // display.textContent = value;
});

function toggleFullScreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen();
    screen.orientation.lock("landscape");
  } else if (document.exitFullscreen) {
    document.exitFullscreen();
    screen.orientation.unlock();
  }
}

function start_timer() {
  const start = Date.now();
  return function () {
    return Date.now() - start;
  }
}

const stick_data = {
    joy_left_x: 0,
    joy_left_y: 0,
    joy_right_x: 0,
    joy_right_y: 0
};

let elapsed_last_send = start_timer(); 

function send_joystick_data() {
    medium.set('joy', stick_data);
    elapsed_last_send = start_timer();
}

let joy_left = new JoyStick('joy_left', {half: "left"}, function(stickData) {
    // console.log(stickData.x);
    // console.log(stickData.y);
    stick_data.joy_left_x = stickData.x;
    stick_data.joy_left_y = stickData.y;

    send_joystick_data();
});

let joy_right = new JoyStick('joy_right', {half: "right"}, function(stickData) {
    // console.log(stickData.x);
    // console.log(stickData.y);
    // display1.textContent = stickData.x;
    // display2.textContent = stickData.y;
    stick_data.joy_right_x = stickData.x;
    stick_data.joy_right_y = stickData.y;

    send_joystick_data();
});

// keepalive send
setInterval(() => {
    if (elapsed_last_send() > 100) { // ms
        send_joystick_data();
    }
}, 10)

if (window.use_webrtc) {
    let signalObj = null;

    function connect_webrtc() {
        if (signalObj)
            return;
 
        let hostname = location.hostname;
        let address = hostname + ':' + (location.port || (location.protocol === 'https:' ? 443 : 8080)) + '/stream/webrtc';
        let protocol = location.protocol === "https:" ? "wss:" : "ws:";
        let wsurl = protocol + '//' + address;

        let video = document.getElementById('camera');

        M.toast({html: "connecting to camera..."});

        signalObj = new signal(wsurl,
            function (stream) {
                // M.Toast.dismissAll();
                M.toast({html: "connected!", classes: "light-green"});
                video.srcObject = stream;
                video.play();
            },
            function (error) {
                // M.Toast.dismissAll();
                M.toast({html: error, classes: "red accent-3"});
                signalObj = null;
            },
            function () {
                console.log('websocket closed. bye bye!');
                video.srcObject = null;
                signalObj = null;
            },
            function (message) {
                // M.Toast.dismissAll();
                M.toast({html: message, classes: "amber lighten-2"});
            }
        );
    }

    connect_webrtc();

    function hangup() {
        if (signalObj) {signalObj.hangup();}
    }

    addEventListener("beforeunload", () => { hangup() }, { capture: true });
    reload_btn.addEventListener('click', e => hangup() );
}
