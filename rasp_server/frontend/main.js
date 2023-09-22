'use strict'
import { Medium } from './medium.js'

const medium = new Medium('http://' + document.domain + ':' + location.port);

const slider = document.getElementById('control_speed');
const display = document.getElementById('display_speed');
const fullscreen_btn = document.getElementById('fullscreen_btn');

slider.addEventListener('input', e => medium.set('speed', Number(slider.value)))

fullscreen_btn.addEventListener('click', e => toggleFullScreen())

medium.subscribe('speed', (value) => {
    slider.value = value;
    display.textContent = value;
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

