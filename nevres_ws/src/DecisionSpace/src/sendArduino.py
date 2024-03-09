import serial
import time

class Arduino:
    def __init__(self):
        self.arduino = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=.5)
        time.sleep(5)
        self.data = [0, 1, 2, 0, 0]
        self.sendData()

    def move(self):
        self.data[0] = 80
        self.data[1] = 1
        self.data[2] = 2

    def sendData(self):
        time.sleep(0.7)
        print(self.data)
        self.arduino.write(self.data)

    def stop(self):
        self.data[0] = 0
        self.data[2] = 1

    def back(self):
        self.data[1] = 2

    def steeringAngle(self, degree):
        self.data[3] = int(degree)

    def leftTurnMax(self):
        self.data[3] = 250  # Max Sol

    def rightTurnMax(self):
        self.data[3] = 5  # Max Sağ

    def leftTurnHalf(self):
        self.data[3] = 187
    
    def rightSignal(self):
        self.data[4] = 3
    
    def signalEmpty(self):
        self.data[4] = 1

    def leftSignal(self):
        self.data[4] = 2

    def rightTurnHalf(self):
        self.data[3] = 63
    
    def straight(self):
        self.data[3] = 125
        
    def emergencyStop(self):
        ##Burada acil stop çalıştırılacak
        return 0
