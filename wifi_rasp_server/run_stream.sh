#!/bin/bash

gunicorn --worker-class eventlet --workers 1 --bind 0.0.0.0:5050 camera_stream_server:app
