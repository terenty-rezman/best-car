import medium
from medium import _app
import serial
from flask import Response
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler


BAUD = 115200
medium.USE_WEBRTC = True # use webrtc frontend for camera


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

    joy_left_x = int(joy["joy_left_x"])
    joy_left_y = int(joy["joy_left_y"])
    joy_right_x = int(joy["joy_right_x"])
    joy_right_y = int(joy["joy_right_y"])

    joy_left_x = int(joy_left_x / 100 * 255)
    joy_left_y = int(joy_left_y / 100 * 255)
    joy_right_x = int(joy_right_x / 100 * 255)
    joy_right_y = int(joy_right_y / 100 * 255)

    joy_left_x = min(255, joy_left_x)
    joy_left_y = min(255, joy_left_y)
    joy_right_x = min(255, joy_right_x)
    joy_right_y = min(255, joy_right_y)

    e1 = joy_left_y + joy_left_x + joy_right_y + joy_right_x 
    e2 = joy_left_y - joy_left_x + joy_right_y - joy_right_x
    e3 = joy_left_y - joy_left_x + joy_right_y + joy_right_x
    e4 = joy_left_y + joy_left_x + joy_right_y - joy_right_x

    e1_direction = 1 if int(e1) > 0 else 2
    e2_direction = 1 if int(e2) < 0 else 2
    e3_direction = 1 if int(e3) < 0 else 2
    e4_direction = 1 if int(e4) > 0 else 2

    e1 = min(255, abs(e1))
    e2 = min(255, abs(e2))
    e3 = min(255, abs(e3))
    e4 = min(255, abs(e4))

    arr = [
        e1, e2, e3, e4, e1_direction, e2_direction, e3_direction, e4_direction
    ]

    write_uart(arr)


def reset_controlling_client():
    global controlling_client

    if not controlling_client:
        return 

    if time.time() - last_controll_time > 1:
        controlling_client = None
        print("control client disconnect")

        # stop the car
        write_uart([0, 0, 0, 0, 0, 0, 0, 0])


scheduler = BackgroundScheduler()
scheduler.add_job(func=reset_controlling_client, trigger="interval", seconds=1)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    medium.listen('0.0.0.0', 80)
