from iviz_msgs.msg import XRHandState
import rospy
import os
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
import roslib; roslib.load_manifest('visualization_marker_tutorials')
import rosbag
from math import nan
from pandas import DataFrame
import pandas as pd

current_directory = os.getcwd() + "/src/iviz_msgs"
# file name of the whole dataset
file_name = "whole_dataset_60_times_rope_gesture_2022-05-24-10-30-17.csv"
df = pd.read_csv(f'{current_directory}/data/{file_name}')


MAX_SAMPLE_COUNTER = len(df)
MAX_COLUMN_COUNTER_L = 188

rospy.init_node('register')
sample_counter = 0
topic = 'visualization_marker_array'
publisher = rospy.Publisher(topic, MarkerArray, queue_size=10)
markerArray = MarkerArray()
marker_size = 0.03

while(sample_counter < MAX_SAMPLE_COUNTER):
    for column_counter in range(5,MAX_COLUMN_COUNTER_L,7):

        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = rospy.get_rostime()
        marker.type = marker.SPHERE
        marker.action = marker.ADD
        marker.scale.x = marker_size
        marker.scale.y = marker_size
        marker.scale.z = marker_size
        marker.color.a = 1.0
        marker.color.r = 0.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        marker.pose.position.x = df.iloc[sample_counter,column_counter]
        marker.pose.position.y = df.iloc[sample_counter,column_counter+1]
        marker.pose.position.z = df.iloc[sample_counter,column_counter+2]
        marker.pose.orientation.w = df.iloc[sample_counter,column_counter+3]
        marker.pose.orientation.x = df.iloc[sample_counter,column_counter+4]
        marker.pose.orientation.y = df.iloc[sample_counter,column_counter+5]
        marker.pose.orientation.z = df.iloc[sample_counter,column_counter+6]
        markerArray.markers.append(marker)

    MAX_COLUMN_COUNTER_R = 369

    for column_counter in range(189,MAX_COLUMN_COUNTER_R,7):

        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = rospy.get_rostime()
        marker.type = marker.SPHERE
        marker.action = marker.ADD
        marker.scale.x = marker_size
        marker.scale.y = marker_size
        marker.scale.z = marker_size
        marker.color.a = 1.0
        marker.color.r = 0.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        marker.pose.position.x = df.iloc[sample_counter,column_counter]
        marker.pose.position.y = df.iloc[sample_counter,column_counter+1]
        marker.pose.position.z = df.iloc[sample_counter,column_counter+2]
        marker.pose.orientation.w = df.iloc[sample_counter,column_counter+3]
        marker.pose.orientation.x = df.iloc[sample_counter,column_counter+4]
        marker.pose.orientation.y = df.iloc[sample_counter,column_counter+5]
        marker.pose.orientation.z = df.iloc[sample_counter,column_counter+6]
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

    # repeat the recording
    sample_counter = sample_counter + 1
    if(sample_counter >= MAX_SAMPLE_COUNTER):
        sample_counter = 0



