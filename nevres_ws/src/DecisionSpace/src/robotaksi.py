#!/usr/bin/env python3
import rospy
from sendArduino import Arduino
from decision import Subscriber
import time
import threading
arduino = Arduino()
subscriber= Subscriber() 



class Robotaksi:
    def __init__(self):
        arduino.steeringAngle(125)
        arduino.sendData()
        time.sleep(6)
        self.imu = 0
        self.rightSignalStatus = False
        self.leftSignalStatus = False
        self.escapeStatus = True

    def stopPlate(self):
        arduino.stop()
        arduino.sendData()
        rospy.sleep(30)

    def rightForced(self):
        if distanceLabel < 3 : 
            arduino.rightTurnHalf()
            time.sleep(1)
            arduino.rightTurnMax()
            arduino.sendData()
    
    def leftForced(self):
        if distanceLabel < 3 :
            arduino.leftTurnHalf()
            arduino.sendData()
            time.sleep(1)
            arduino.leftTurnMax()
            arduino.sendData()    

    def leftSignal(self):
        while self.leftSignalStatus:
            arduino.leftSignal()
            time.sleep(0.5)
            arduino.signalEmpty()
            time.sleep(0.5)
 
    def rightSignal(self):
       while self.rightSignalStatus:
            arduino.rightSignal()
            time.sleep(0.5)
            arduino.signalEmpty()
            time.sleep(0.5)

    def rightChangeLanes(self,imuDegree):
        self.rightSignalStatus = True
        solThred = threading.Thread(target=self.rightSignal)
        solThred.start()

        arduino.rightTurnMax()
        arduino.sendData()
        self.rightSignalStatus = False
        time.sleep(1.5)
        arduino.leftTurnMax()
        arduino.sendData()     
        time.sleep(3)  

    def leftChangeLanes(self,imuDegree):
        self.leftSignalStatus = True
        solThred = threading.Thread(target=self.leftSignal)
        solThred.start()

        arduino.leftTurnMax()
        arduino.sendData()
        time.sleep(1.5)
        self.leftSignalStatus = False
        arduino.rightTurnMax()
        arduino.sendData()
        time.sleep(3)
            
    def stop(self):
        arduino.stop()
        arduino.sendData()

    def move(self):
        if subscriber.sagLane < 182:
            arduino.steeringAngle(135)
            arduino.sendData()
        elif subscriber.sagLane > 192:
            arduino.steeringAngle(110)
            arduino.sendData()
        elif subscriber.sagLane < 167:
            arduino.leftTurnHalf()
            arduino.sendData()
        else: 
            arduino.steeringAngle(125)
        arduino.move()
        arduino.sendData()
        time.sleep(4)

    def straight():
        arduino.straight()
        arduino.sendData()

    def escapeObstancle(self,imu):
        if self.escapeStatus:
            self.imu = imu
           
            if subscriber.sagLane < 180:
                self.leftChangeLanes(imu)
            elif subscriber.sagLane > 190:
                self.rightChangeLanes(imu)

        self.escapeStatus = False

    def forwardRightForced():
        pass

    def forwardLeftForced():
        pass

    def station(self):
        if distanceLabel < 5 : 
            arduino.rightTurnHalf()
            arduino.sendData()
            time.sleep(1)
            arduino.leftTurnMax()
            arduino.sendData()
            time.sleep(1)
            arduino.stop()
            arduino.sendData()
            time.sleep(32)
            arduino.leftTurnMax()
            arduino.sendData()
            time.sleep(0.5)
            arduino.rightTurnMax()
            arduino.sendData()

    
robotaksi = Robotaksi()

label_actions = {
    1: robotaksi.escapeObstancle,
    2: robotaksi.stopPlate,
    3: robotaksi.station,
    5: robotaksi.leftForced,
    6: lambda: robotaksi.forwardRightForced(imuValue),
    7: lambda: robotaksi.forwardLeftForced(imuValue),
    8: robotaksi.stop,
    11: robotaksi.leftForced,
    12: robotaksi.rightForced,
    13: robotaksi. rightForced,
    14: robotaksi.leftForced,
    17: robotaksi.move,


}
while True:
    distance = subscriber.obstancle 
    imuValue = subscriber.imuDegree
    label_array = subscriber.indexLabel
    distanceLabel = subscriber.plateDistance
  
    if 0.0 < distance < 7:  
        robotaksi.escapeObstancle(imuValue)  
    else:
        if label_array == 8:
            if distanceLabel < 5:
                robotaksi.stop()
        elif label_array == 17:
            robotaksi.move()
        elif label_array == 9:
            robotaksi.station()
        else:
            robotaksi.move()  
            arduino.sendData()

            if len(label_array) == 2:  # İki Tabela Algılandıysa
                if set(label_array) == {5, 11}:  
                    robotaksi.leftForced()
                elif set(label_array) == {5, 12}:  
                    robotaksi.rightForced()
                elif set(label_array) == {5, 13}:  
                    robotaksi.rightForced()
                elif set(label_array) == {5, 14}:  
                    robotaksi.leftForced()
                elif set(label_array) == {11, 13}:  
                    robotaksi.straight()
                elif set(label_array) == {15, 12}:  
                    robotaksi.rightForced()
                elif set(label_array) == {15, 13}:  
                    robotaksi.rightForced()
                elif set(label_array) == {15, 14}:  
                    robotaksi.leftForced()
            elif len(label_array) == 3:  # Üç Tabela Algılandıysa
                pass
            elif len(label_array) == 1:  # Bir Tabela Algılandıysa
                label_index = label_array[0]
                for i, distanceL in enumerate(distanceLabel):
                    label_actions = {5: robotaksi.leftForced, 11: robotaksi.straight, 12: robotaksi.rightForced,
                                     13: robotaksi.rightForced, 14: robotaksi.leftForced}
                    if i == label_index and label_index in label_actions:
                        if distanceL < 6:
                            label_actions[label_index](imuValue)
                        else:
                            robotaksi.move()
                    else:
                        robotaksi.move()
