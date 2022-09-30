#!/usr/bin/env python3

import rospy
import math
import tf
from geometry_msgs.msg import PoseStamped

path_filename = "/home/davesarmoury/Desktop/utm_path.txt"
parent_link = "utm"
child_link = "map"

path = [
    [4.400091171264648, 0.00405120849609375, 0.0, 0.0, 0.0, -0.9227876400930938, 0.38530892968035246],
    [2.781132698059082, -1.3798370361328125, 0.0, 0.0, 0.0, -0.8864971681218381, 0.4627340174570716],
    [1.8618230819702148, -2.5897960662841797, 0.0, 0.0, 0.0, -0.7813467960561667, 0.6240970952446125],
    [2.796586036682129, -5.035957336425781, 0.0, 0.0, 0.0, 0.0747718964159161, 0.9972006636110746],
    [4.60018253326416, -4.260416030883789, 0.0, 0.0, 0.0, 0.4050031113301335, 0.9143153065616432],
    [5.878782272338867, -2.6930580139160156, 0.0, 0.0, 0.0, 0.5035542500988184, 0.8639636087286412],
    [7.442048072814941, -0.7235088348388672, 0.0, 0.0, 0.0, 0.5507742055453538, 0.8346542844231283],
    [8.386674880981445, 1.3340034484863281, 0.0, 0.0, 0.0, 0.5326155616703641, 0.846357290667814],
    [8.545239448547363, 3.3503036499023438, 0.0, 0.0, 0.0, 0.8604613941903562, 0.5095156416715668]
]

pos_tolerance = 2.0

def dist(trans, pose):
    distance = math.sqrt( (trans[0] - pose[0]) ** 2 +  (trans[1] - pose[1]) ** 2 +  (trans[2] - pose[2]) ** 2 )
    return distance

def getPoseStamped(data):
    ps = PoseStamped()
    ps.header.stamp = rospy.Time.now()
    ps.header.frame_id = "map"
    ps.pose.position.x = data[0]
    ps.pose.position.y = data[1]
    ps.pose.position.z = data[2]
    ps.pose.orientation.x = data[3]
    ps.pose.orientation.y = data[4]
    ps.pose.orientation.z = data[5]
    ps.pose.orientation.w = data[6]
    return ps

def main():
    outFile = open(path_filename, 'w')
    outFile.close()

    rospy.init_node('utm_driver')
    pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)

    listener = tf.TransformListener()
    listener.waitForTransform("map", "base_link", rospy.Time(), rospy.Duration(10.0))

    rate = rospy.Rate(2.0)
    pindex = 0
    while not rospy.is_shutdown() and pindex < len(path):
        try:
            (trans,rot) = listener.lookupTransform("map", "base_link", rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        pub.publish(getPoseStamped(path[pindex]))

        if dist(trans, path[pindex]) <= pos_tolerance:
            pindex = pindex + 1

        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
