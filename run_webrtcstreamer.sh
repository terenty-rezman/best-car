#!/bin/bash

docker run --device=/dev/video0 --net=host -it mpromonet/webrtc-streamer -u "videocap://0"
