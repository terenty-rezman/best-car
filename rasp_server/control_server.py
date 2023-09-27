import medium
from medium import _app
import serial
from flask import Response

BAUD = 115200


# connect to stm32 via UART
ser = serial.Serial('/dev/ttyAMA0', BAUD)  # open serial port
print(ser.name)

medium.set('speed', 0)


@medium.subscribe('speed')
def speedUpdated(value):
    print('speed =', value)

    as_bytes = bytes([min(255, value)])
    ser.write(as_bytes)


if __name__ == "__main__":
    medium.listen('0.0.0.0', 5000)
