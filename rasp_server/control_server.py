import medium
from medium import _app
import serial
from flask import Response
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler


BAUD = 115200
medium.USE_WEBRTC = True

# connect to stm32 via UART
ser = serial.Serial('/dev/ttyAMA0', BAUD, write_timeout=0)  # open serial port
print(ser.name)

medium.set('joy', {})


controlling_client = None
last_controll_time = time.time()


def write_uart(arr: list):
    if ser.isOpen() == False:
        return

    as_bytes = bytes(arr)
    written = ser.write(as_bytes)


@medium.on_disconnect()
def client_disconnected(cliend_sid):
    global controlling_client
    if controlling_client == cliend_sid:
        controlling_client = None


@medium.subscribe('joy')
def joyUpdated(joy, client_sid):
    global controlling_client
    global last_controll_time

    if not controlling_client:
        controlling_client = client_sid
        print("new control client:", client_sid)
    
    if controlling_client != client_sid:
        return
    
    last_controll_time = time.time()

    joy_left_x = abs(int(joy["joy_left_x"]))
    joy_left_y = abs(int(joy["joy_left_y"]))
    joy_right_x = abs(int(joy["joy_right_x"]))
    joy_right_y = abs(int(joy["joy_right_y"]))

    joy_left_x = int(joy_left_x / 100 * 255)
    joy_left_y = int(joy_left_y / 100 * 255)
    joy_right_x = int(joy_right_x / 100 * 255)
    joy_right_y = int(joy_right_y / 100 * 255)

    joy_left_x = min(255, joy_left_x)
    joy_left_y = min(255, joy_left_y)
    joy_right_x = min(255, joy_right_x)
    joy_right_y = min(255, joy_right_y)

    joy_left_x_negative = 1 if int(joy["joy_left_x"]) < 0 else 0
    joy_left_y_negative = 1 if int(joy["joy_left_y"]) < 0 else 0
    joy_right_x_negative = 1 if int(joy["joy_right_x"]) < 0 else 0
    joy_right_y_negative = 1 if int(joy["joy_right_y"]) < 0 else 0

    arr = [
        joy_left_x, joy_left_y, joy_right_x, joy_right_y, joy_left_x_negative, joy_left_y_negative, joy_right_x_negative, joy_right_y_negative
    ]

    # arr = [
    #     201, 202, 203, 204, 1, 2, 3, 4
    # ]

    write_uart(arr)


def reset_controlling_client():
    global controlling_client

    if not controlling_client:
        return 

    if time.time() - last_controll_time > 1:
        controlling_client = None
        print("control client disconnect")
        write_uart([0, 0, 0, 0, 0, 0, 0, 0])


scheduler = BackgroundScheduler()
scheduler.add_job(func=reset_controlling_client, trigger="interval", seconds=1)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    medium.listen('0.0.0.0', 80)
