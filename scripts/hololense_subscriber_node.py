from iviz_msgs.msg import XRHandState
import rospy
import os
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
import roslib; roslib.load_manifest('visualization_marker_tutorials')
import rosbag
from math import nan
from pandas import DataFrame



def callback(data):
    print("Daten kommen an")

    rospy.loginfo("Palm x: %f, Palm y: %f, Palm z: %f, Palm quaternion: %f", data.palm.translation.x,
    data.palm.translation.y, data.palm.translation.z, data.palm.rotation.x)
    marker = Marker()
    marker.header.frame_id = "map"
    marker.header.stamp = rospy.get_rostime()
    marker.type = marker.SPHERE
    marker.action = marker.ADD
    marker.scale.x = 0.1
    marker.scale.y = 0.1
    marker.scale.z = 0.1
    marker.color.a = 1.0
    marker.color.r = 0.0
    marker.color.g = 0.0
    marker.color.b = 1.0
    marker.pose.position.x = data.palm.translation.x
    marker.pose.position.y = data.palm.translation.y
    marker.pose.position.z = data.palm.translation.z
    marker.pose.orientation.w = 1
    markerArray.markers.append(marker)

    for i in range (4):
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = rospy.get_rostime()
        marker.type = marker.SPHERE
        marker.action = marker.ADD
        marker.scale.x = 0.05
        marker.scale.y = 0.05
        marker.scale.z = 0.05
        marker.color.a = 1.0
        marker.color.r = 0.0
        marker.color.g = 0.0
        marker.color.b = 1.0
        marker.pose.position.x = data.thumb[i].translation.x
        marker.pose.position.y = data.thumb[i].translation.y
        marker.pose.position.z = data.thumb[i].translation.z
        marker.pose.orientation.w = 1
        markerArray.markers.append(marker)

    
    # Renumber the marker IDs
    id = 0
    for m in markerArray.markers:
        m.id = id
        id += 1

    # Publish the MarkerArray
    publisher.publish(markerArray)
    # marker muss vor jedem neuen pushen gecleart werden
    markerArray.markers.clear()

def listener():
    rospy.init_node('register')
    rospy.Subscriber('/iviz_win_vr/xr/left_hand', XRHandState, callback)
    rospy.spin()

topic = 'visualization_marker_array'
publisher = rospy.Publisher(topic, MarkerArray, queue_size=10)
if __name__ == '__main__':
    markerArray = MarkerArray()

    #subscriber anschalten
    try:
       listener()
    except rospy.ROSInterruptException:
       pass
    


