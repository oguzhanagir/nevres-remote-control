import serial
import time

arduino = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=.5)
time.sleep(5)


data = [70,1,2,10,0]
print(data)
time.sleep(0.5)
arduino.write(data)