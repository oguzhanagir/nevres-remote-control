#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan

class Lidar:

    def __init__(self):
        rospy.init_node('scan_listener',anonymous=True  )
        self.distances = []

        self.pub = rospy.Publisher('obstancle_distance', Float64, queue_size=10)
        # self.pub_right = rospy.Publisher('right_distance', Float64, queue_size=10)

        rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        
        rospy.spin()

    def scan_callback(self,msg):
        self.distances = []
        self.rightDistances = []


        for i in range(500,600,4):
            
            if msg.ranges[i] > 0.0:
                
                self.distances.append(msg.ranges[i])
                self.pub.publish(min(self.distances))
              
          
        # for i in range(1,135,1):
        #     if msg.ranges[i] > 0.0 :
        #         self.rightDistances.append(msg.ranges[i])
        #         self.pub_right.publish(min(self.rightDistances))
    


Lidar()







