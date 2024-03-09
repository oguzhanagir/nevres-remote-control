#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64,Float32MultiArray,Int64


class Subscriber:
    def __init__(self):
        rospy.init_node('decision_subscriber', anonymous=True)
        ## Trafik Levhası Label ve Mesafe Bİlgisi
        rospy.Subscriber('plate_index', Float32MultiArray, self.plateIndexDetect)
        rospy.Subscriber('plate_distance', Float32MultiArray, self.plateDistanceDetect)

        # ## Lidar Ön, Sol, Sağ Mesafe Değerleri 
        rospy.Subscriber('obstancle_distance', Float64, self.obstancleDetect)
        # ## Şerit Orta Nokta Değeri
        rospy.Subscriber('lane_index', Float64, self.laneDetect)

        # ## İvme Sensör Değeri
        # rospy.Subscriber('imu_degree', Float64, self.imuValue)
     


        self.obstancle = 0.0
        self.plateDistance = 0.0
        self.indexLabel = 0
        self.solLane = 0.0
        self.sagLane = 0.0
     
        self.right_distance_lidar = 0.0
        self.distance = 0

        self.imuDegree = 0

    def obstancleDetect(self, msg):        
        self.obstancle = msg.data
        
    def rightDistance(self, rightDistance):
        self.right_distance_lidar = rightDistance
        
    def returnObstancle(self): 
        return self.obstancle
    
    def plateIndexDetect(self, indexPlateArray):
        for index in indexPlateArray.data:
            self.indexLabel = index
    
    def plateDistanceDetect(self,plateDistance):
        for self.distance in plateDistance.data:
            self.plateDistance = self.distance
    
    def laneDetect(self,laneMiddleDot):
        self.solLane = laneMiddleDot.data[0]
        self.sagLane = laneMiddleDot.data[1]

    def imuValue(self,imuSensor):
        self.imuSensorValue = imuSensor.data
        print(self.imuSensorValue)
    
    def rightDistanceLidar(self,rightDistance):
        self.right_distance_lidar = rightDistance
    
    def leftDistanceLidar(self,leftDistance):
        self.left_distance_lidar = leftDistance



if __name__ == '__main__':
    subscriber = Subscriber()
    rospy.spin()
