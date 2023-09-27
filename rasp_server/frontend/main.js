'use strict'
import { Medium } from './medium.js'

const medium = new Medium('http://' + document.domain + ':' + location.port);

const slider = document.getElementById('control_speed');
const display1 = document.getElementById('display1');
const display2 = document.getElementById('display2');
const fullscreen_btn = document.getElementById('fullscreen_btn');

const camera = document.getElementById('camera');
camera.src = window.location.protocol + "//" + window.location.hostname + ":5050/video_feed"

// slider.addEventListener('input', e => medium.set('speed', Number(slider.value)))

fullscreen_btn.addEventListener('click', e => toggleFullScreen())

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

let joy1 = new JoyStick('joy1Div', {half: "left"}, function(stickData) {
    // console.log(stickData.x);
    // console.log(stickData.y);
});

let joy2 = new JoyStick('joy2Div', {half: "right"}, function(stickData) {
    // console.log(stickData.x);
    // console.log(stickData.y);
    display1.textContent = stickData.x;
    display2.textContent = stickData.y;
});
