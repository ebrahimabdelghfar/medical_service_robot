#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float32,Float32MultiArray,Int32
condition=0
con2=1
def proximity_sensor(msg):
    global condition
    global con2
    condition=msg.data
    if (condition==1 and con2==1):
        motor_RL.publish(0)
        motor_FL.publish(0)
        motor_RR.publish(0)
        motor_FR.publish(0)
        rospy.sleep(2)
        degree_of_opening=-0.51
        box[0].publish(degree_of_opening)
        box[1].publish(degree_of_opening)
        box[3].publish(degree_of_opening)
        rospy.sleep(10)
        box[0].publish(origin_of_boxes[0])
        box[1].publish(origin_of_boxes[1])
        box[3].publish(origin_of_boxes[3])
        rospy.sleep(10)
        motor_RL.publish(7)
        motor_FL.publish(7)
        motor_RR.publish(7)
        motor_FR.publish(7)
        rospy.sleep(3)
        condition=0
        con2=0

        


#initiate the node and publisher
rospy.init_node("serve_pills")
box1=rospy.Publisher("/sim_ros_interface/box1/setpoint_position",Float32,queue_size=50)
box2=rospy.Publisher("/sim_ros_interface/box2/setpoint_position",Float32,queue_size=50)
box3=rospy.Publisher("/sim_ros_interface/box3/setpoint_position",Float32,queue_size=50)
box4=rospy.Publisher("/sim_ros_interface/box4/setpoint_position",Float32,queue_size=50)

#motor publisher
motor_FL=rospy.Publisher("/sim_ros_interface/FL_J/setpoint_speed",Float32,queue_size=50)
motor_RL=rospy.Publisher("/sim_ros_interface/RL_J/setpoint_speed",Float32,queue_size=50)
motor_FR=rospy.Publisher("/sim_ros_interface/FR_J/setpoint_speed",Float32,queue_size=50)
motor_RR=rospy.Publisher("/sim_ros_interface/RR_J/setpoint_speed",Float32,queue_size=50)

box=[box1,box2,box3,box4]
origin=Float32MultiArray
origin_of_boxes=[-2.19,-2.35,-2.3038,-2.373]
#initation end
degree_of_opening=Float32
if __name__== "__main__" :
    rospy.Subscriber("/sim_ros_interface/proximity_sensor/state",Int32,proximity_sensor)
    rospy.spin()
