#!/usr/bin/env python3

import rospy
import math
import tf
import geometry_msgs.msg
import turtlesim.srv

path_filename = "/home/davesarmoury/Desktop/utm_path.txt"
parent_link = "utm"
child_link = "base_link"

def main():
    outFile = open(path_filename, 'w')
    outFile.close()

    rospy.init_node('utm_saver')

    listener = tf.TransformListener()

    listener.waitForTransform(parent_link, child_link, rospy.Time(), rospy.Duration(10.0))

    rate = rospy.Rate(2.0)
    while not rospy.is_shutdown():
        try:
            (trans,rot) = listener.lookupTransform(parent_link, child_link, rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        outFile = open(path_filename, 'a+')
        outFile.write(str(trans) + "," + str(rot) + "\n")
        outFile.close()

        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
