#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32,Float32


def IR_R(msg):
    l=msg.data
    avg=0.45
    speed=Float32
    speed=2
    if (l<avg):
    #RIGHT FASTER
        motor_RL.publish(-1*speed)
        motor_FL.publish(-1*speed)
        motor_RR.publish(speed/2.2)
        motor_FR.publish(speed/2.2)
        rospy.loginfo(l)





rospy.init_node("line_follower11")

#motor publisher
motor_FL=rospy.Publisher("/sim_ros_interface/FL_J/setpoint_speed",Float32,queue_size=50)
motor_RL=rospy.Publisher("/sim_ros_interface/RL_J/setpoint_speed",Float32,queue_size=50)
motor_FR=rospy.Publisher("/sim_ros_interface/FR_J/setpoint_speed",Float32,queue_size=50)
motor_RR=rospy.Publisher("/sim_ros_interface/RR_J/setpoint_speed",Float32,queue_size=50)
#sensor subscriber

if __name__== "__main__" :
    r=rospy.Subscriber("/sim_ros_interface/IR_R",Float32,IR_R)
    rospy.spin()


