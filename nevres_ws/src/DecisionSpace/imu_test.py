#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64,Float32MultiArray,Int64


class Imu:

    def __init__(self): 
        rospy.init_node('imu', anonymous=True)
        ## İvme Sensör Değeri
        rospy.Subscriber('imu_degree', Float64, self.imuValue)
        self.imuDegree = 0
        rospy.spin()
    def imuValue(self,data):
        self.imuDegree = data.data
        print(self.imuDegree)


Imu()
