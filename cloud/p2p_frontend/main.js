'use strict'

const video_streamer = new raspi_video_stream("#remoteStream");
video_streamer.connect();

const controls = new control_stream();
controls.connect();
