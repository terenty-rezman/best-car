import medium
import wiringpi
import serial

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


medium.listen('0.0.0.0', 5000)
