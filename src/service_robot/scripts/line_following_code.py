#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32,Float32

def IR_L(msg):
    r=msg.data
    avg=0.45
    speed=Float32
    speed=2
    if (r<avg): 
    #LEFT FASTER
        motor_RR.publish(speed)
        motor_FR.publish(speed)
        motor_RL.publish(-1*speed/2.2)
        motor_FL.publish(-1*speed/2.2)

rospy.init_node("line_follower")

#motor publisher
motor_FL=rospy.Publisher("/sim_ros_interface/FL_J/setpoint_speed",Float32,queue_size=50)
motor_RL=rospy.Publisher("/sim_ros_interface/RL_J/setpoint_speed",Float32,queue_size=50)
motor_FR=rospy.Publisher("/sim_ros_interface/FR_J/setpoint_speed",Float32,queue_size=50)
motor_RR=rospy.Publisher("/sim_ros_interface/RR_J/setpoint_speed",Float32,queue_size=50)
#sensor subscriber
if __name__== "__main__" :
    l=rospy.Subscriber("/sim_ros_interface/IR_L",Float32,IR_L)
    rospy.spin()


