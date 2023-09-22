'use strict'
import { Medium } from './medium.js'

const medium = new Medium('http://' + document.domain + ':' + location.port);

const slider = document.getElementById('control_speed');
const display = document.getElementById('display_speed');
const stop_btn = document.getElementById('stop_btn');

slider.addEventListener('input', e => medium.set('speed', Number(slider.value)))

// stop_btn.addEventListener('click', e => medium.set('speed', Number(0)))

medium.subscribe('speed', (value) => {
    slider.value = value;
    display.textContent = value;
});
