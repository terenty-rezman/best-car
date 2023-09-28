import medium
from medium import _app
import serial
from flask import Response
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler


BAUD = 115200


# connect to stm32 via UART
ser = serial.Serial('/dev/ttyAMA0', BAUD)  # open serial port
print(ser.name)

medium.set('joy', {})


controlling_client = None
last_controll_time = time.time()


@medium.on_disconnect()
def client_disconnected(cliend_sid):
    global controlling_client
    if controlling_client == cliend_sid:
        controlling_client = None


@medium.subscribe('joy')
def joyUpdated(joy, client_sid):
    # print(joy)

    global controlling_client
    global last_controll_time

    if not controlling_client:
        controlling_client = client_sid
        print("new control client:", client_sid)
    
    if controlling_client != client_sid:
        return
    
    last_controll_time = time.time()

    value = min(255, abs(int(joy["joy_right_y"])))

    as_bytes = bytes([value])
    ser.write(as_bytes)


def reset_controlling_client():
    global controlling_client

    if not controlling_client:
        return 

    if time.time() - last_controll_time > 1:
        controlling_client = None
        print("control client disconnect")


scheduler = BackgroundScheduler()
scheduler.add_job(func=reset_controlling_client, trigger="interval", seconds=1)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    medium.listen('0.0.0.0', 80)
