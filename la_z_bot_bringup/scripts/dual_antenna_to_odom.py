#!/usr/bin/env python3

import rospy
from microstrain_inertial_msgs.msg import GNSSDualAntennaStatus
from nav_msgs.msg import Odometry
from tf.transformations import quaternion_from_euler

def Average(lst):
    return sum(lst) / len(lst)

def callback(msg):
    global pub
    odom_msg = Odometry()
    odom_msg.header.stamp = rospy.Time.now()
    odom_msg.header.frame_id = "utm"
    odom_msg.child_frame_id = "gq7_link"

    q = quaternion_from_euler(0, 0, msg.heading)

    odom_msg.pose.pose.orientation.x = q[0]
    odom_msg.pose.pose.orientation.y = q[1]
    odom_msg.pose.pose.orientation.z = q[2]
    odom_msg.pose.pose.orientation.w = q[3]

    odom_msg.pose.covariance[35] = msg.heading_uncertainty

    pub.publish(odom_msg)

def main():
    global pub
    rospy.init_node('dual_antenna_to_odom', anonymous=True)
    rospy.Subscriber("/nav/dual_antenna_status", GNSSDualAntennaStatus, callback)
    pub = rospy.Publisher('/nav/dual_antenna_odom', Odometry, queue_size=10)

    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
