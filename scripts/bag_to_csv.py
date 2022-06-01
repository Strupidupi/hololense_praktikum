from fileinput import filename
import numpy as np
import os
import pandas as pd
from pandas import DataFrame
from math import nan

from yaml import load
import rosbag


def return_data(file_name = '60_times_right_hand_left_swipe_gesture_2022-05-24-10-24-47.bag'):
    def rotate_to_head(t_x, t_y, t_z, r_x, r_y, r_z, r_w, t_head, q_head):
        # q = Quaternion(r_x, r_y, r_z, r_w)
        # t = np.array([t_x, t_y, t_z])
        #
        # q_new, t_new = q_head.inverse * q, q_head.inverse.rotate(-t) + t_head
        #
        # t_x, t_y, t_z = t_new[0], t_new[1], t_new[2]
        # r_x, r_y, r_z, r_w = q_new[0], q_new[1], q_new[2], q_new[3]

        return t_x, t_y, t_z, r_x, r_y, r_z, r_w


    # TODO:current_directory eventualy has to be set to the corrcet_directory !!!
    current_directory = os.getcwd() + "/src/iviz_msgs"
    bag = rosbag.Bag(current_directory + f'/data/{file_name}')

    # segments: 'palm', 'thumb', 'index', 'middle', 'ring', 'little'
    # build columns
    columns = ['secs', 'nsecs', 'is_valid', 'palm_j0_t_x', 'palm_j0_t_y', 'palm_j0_t_z', 'palm_j0_r_x', 'palm_j0_r_y', 'palm_j0_r_z', 'palm_j0_r_w']

    for i in range(5):
        columns.extend([f'thumb_j{i}_t_x', f'thumb_j{i}_t_y', f'thumb_j{i}_t_z', f'thumb_j{i}_r_x', f'thumb_j{i}_r_y',
                        f'thumb_j{i}_r_z', f'thumb_j{i}_r_w'])
    for i in range(5):
        columns.extend([f'index_j{i}_t_x', f'index_j{i}_t_y', f'index_j{i}_t_z', f'index_j{i}_r_x', f'index_j{i}_r_y',
                        f'index_j{i}_r_z', f'index_j{i}_r_w'])
    for i in range(5):
        columns.extend(
            [f'middle_j{i}_t_x', f'middle_j{i}_t_y', f'middle_j{i}_t_z', f'middle_j{i}_r_x', f'middle_j{i}_r_y',
             f'middle_j{i}_r_z', f'middle_j{i}_r_w'])
    #
    for i in range(5):
        columns.extend([f'ring_j{i}_t_x', f'ring_j{i}_t_y', f'ring_j{i}_t_z', f'ring_j{i}_r_x', f'ring_j{i}_r_y',
                        f'ring_j{i}_r_z', f'ring_j{i}_r_w'])

    for i in range(5):
        columns.extend(
            [f'little_j{i}_t_x', f'little_j{i}_t_y', f'little_j{i}_t_z', f'little_j{i}_r_x', f'little_j{i}_r_y',
             f'little_j{i}_r_z', f'little_j{i}_r_w'])

    # rename the columns, so that left and right can be distinguished example: L_thumb_j0_t_x and R_thumb_j0_t_x 
    columns_L = list(map(lambda x: "L_" + x if ( not (x == "secs" or x == "nsecs")) else x ,columns))
    columns_R = list(map(lambda x: "R_" + x if ( not (x == "secs" or x == "nsecs")) else x ,columns))   
    columns_tf = ['secs', 'nsecs', 'translation_x', 'translation_y', 'translation_z', 'rotation_x', 'rotation_y', 'rotation_z', 'rotation_w' ]

    data = {'left_hand': DataFrame(data=None, index=None, columns=columns_L, dtype=None, copy=False),
            'right_hand': DataFrame(data=None, index=None, columns=columns_R, dtype=None, copy=False),
            'tf': DataFrame(data=None, index=None, columns=columns_tf, dtype=None, copy=False)}

    counter = 0
    q_head, t_head = 0, 0


    # build dataframy by appending rows
    for topic, msg, t in bag.read_messages():
        ### TODO: Basischange
        # if topic == '/tf':
        #     m = msg.transforms[-1].transform

        #     # rotation and translation of head
        #     r_x, r_y, r_z, r_w = m.rotation.x, m.rotation.y, m.rotation.z, m.rotation.w
        #     t_x, t_y, t_z = m.translation.x, m.translation.y, m.translation.z

        #     q_head = Quaternion(r_x, r_y, r_z, r_w)
        #     t_head = np.array([t_x, t_y, t_z])

        # get the coresponding tf for every timestamp
        if(topic == "/tf"):
            row = []
            row.extend([msg.transforms[-1].header.stamp.secs, msg.transforms[-1].header.stamp.nsecs, msg.transforms[-1].transform.translation.x,
            msg.transforms[-1].transform.translation.y, msg.transforms[-1].transform.translation.z, msg.transforms[-1].transform.rotation.x, msg.transforms[-1].transform.rotation.y, 
            msg.transforms[-1].transform.rotation.z, msg.transforms[-1].transform.rotation.w])

            data["tf"].loc[counter] = row

        for key in data.keys():
            if topic == f'/iviz_win_vr/xr/{key}':
                row = []
                row.extend([ msg.header.stamp.secs, msg.header.stamp.nsecs, msg.is_valid])

                if msg.palm:
                    t_x, t_y, t_z = msg.palm.translation.x, msg.palm.translation.y, msg.palm.translation.z
                    r_x, r_y, r_z, r_w = msg.palm.rotation.x, msg.palm.rotation.y, msg.palm.rotation.z, \
                                         msg.palm.rotation.w

                    t_x, t_y, t_z, r_x, r_y, r_z, r_w = rotate_to_head(t_x, t_y, t_z, r_x,
                                                                       r_y, r_z, r_w, t_head, q_head)

                    row.extend([t_x, t_y, t_z, r_x, r_y, r_z, r_w])
                else:
                    for i in range(7):
                        row.append(nan)

                if msg.thumb:
                    for i in range(len(msg.thumb)):
                        t_x, t_y, t_z = msg.thumb[i].translation.x, msg.thumb[i].translation.y, msg.thumb[i].translation.z
                        r_x, r_y, r_z, r_w = msg.thumb[i].rotation.x, msg.thumb[i].rotation.y, msg.thumb[i].rotation.z, \
                                             msg.thumb[i].rotation.w
                        t_x, t_y, t_z, r_x, r_y, r_z, r_w = rotate_to_head(t_x, t_y, t_z, r_x,
                                                                           r_y, r_z, r_w, t_head, q_head)

                        row.extend([t_x, t_y, t_z, r_x, r_y, r_z, r_w])
                else:
                    for i in range(35):
                        row.append(nan)

                if msg.index:
                    for i in range(len(msg.index)):
                        t_x, t_y, t_z = msg.index[i].translation.x, msg.index[i].translation.y, msg.index[i].translation.z
                        r_x, r_y, r_z, r_w = msg.index[i].rotation.x, msg.index[i].rotation.y, msg.index[i].rotation.z, \
                                             msg.index[i].rotation.w
                        t_x, t_y, t_z, r_x, r_y, r_z, r_w = rotate_to_head(t_x, t_y, t_z, r_x,
                                                                           r_y, r_z, r_w, t_head, q_head)
                        row.extend([t_x, t_y, t_z, r_x, r_y, r_z, r_w])
                else:
                    for i in range(35):
                        row.append(nan)

                if msg.middle:
                    for i in range(len(msg.middle)):
                        t_x, t_y, t_z = msg.middle[i].translation.x, msg.middle[i].translation.y, msg.middle[
                            i].translation.z
                        r_x, r_y, r_z, r_w = msg.middle[i].rotation.x, msg.middle[i].rotation.y, msg.middle[i].rotation.z, \
                                             msg.middle[i].rotation.w
                        t_x, t_y, t_z, r_x, r_y, r_z, r_w = rotate_to_head(t_x, t_y, t_z, r_x,
                                                                           r_y, r_z, r_w, t_head, q_head)
                        row.extend([t_x, t_y, t_z, r_x, r_y, r_z, r_w])
                else:
                    for i in range(35):
                        row.append(nan)

                if msg.ring:
                    for i in range(len(msg.ring)):
                        t_x, t_y, t_z = msg.ring[i].translation.x, msg.ring[i].translation.y, msg.ring[i].translation.z
                        r_x, r_y, r_z, r_w = msg.ring[i].rotation.x, msg.ring[i].rotation.y, msg.ring[i].rotation.z, \
                                             msg.ring[i].rotation.w
                        t_x, t_y, t_z, r_x, r_y, r_z, r_w = rotate_to_head(t_x, t_y, t_z, r_x,
                                                                           r_y, r_z, r_w, t_head, q_head)
                        row.extend([t_x, t_y, t_z, r_x, r_y, r_z, r_w])
                else:
                    for i in range(35):
                        row.append(nan)

                if msg.little:
                    for i in range(len(msg.little)):
                        t_x, t_y, t_z = msg.little[i].translation.x, msg.little[i].translation.y, msg.little[
                            i].translation.z
                        r_x, r_y, r_z, r_w = msg.little[i].rotation.x, msg.little[i].rotation.y, msg.little[i].rotation.z, \
                                             msg.little[i].rotation.w
                        t_x, t_y, t_z, r_x, r_y, r_z, r_w = rotate_to_head(t_x, t_y, t_z, r_x,
                                                                           r_y, r_z, r_w, t_head, q_head)
                        row.extend([t_x, t_y, t_z, r_x, r_y, r_z, r_w])
                else:
                    for i in range(35):
                        row.append(nan)

                data[key].loc[counter] = row
        counter += 1
    bag.close()

    return data

def save_data_to_csv(file_name):
    data = return_data(file_name)
    # rename file.bag to file.csv
    file_name = file_name.replace(".bag",".csv")
    current_directory = os.getcwd() + "/src/iviz_msgs"
    data['left_hand'].to_csv(current_directory + "/data/left_hand_" + file_name)
    data['right_hand'].to_csv(current_directory + "/data/right_hand_" + file_name)
    data['tf'].to_csv(current_directory + "/data/tf_" + file_name)
    print('data saved')
    merge_tables(file_name)

def merge_tables(file_name):
    current_directory = os.getcwd() + "/src/iviz_msgs"
    df_L = pd.read_csv(f'{current_directory}/data/left_hand_{file_name}')
    df_R = pd.read_csv(f'{current_directory}/data/right_hand_{file_name}')
    df_tf = pd.read_csv(f'{current_directory}/data/tf_{file_name}')
    result = pd.merge(df_L, df_R, on=["secs", "nsecs"], how="outer")
    result = pd.merge(result, df_tf, on=["secs", "nsecs"], how="outer")
    result.to_csv(current_directory + "/data/whole_dataset_" + file_name)

def extract_single_movements(file_name):
    print("Filename ist: " + file_name)
    current_directory = os.getcwd() + "/src/iviz_msgs"
    # make new dir 
    path = current_directory + "/data/" + file_name.replace(".csv","")
    if not os.path.exists(path):
        os.makedirs(path)

    # bei klapp_gesture und rope_gesture cutten wenn eine von beiden Händen nicht mehr sichtbar ist
    if(("klapp_gesture" in file_name) or ("rope_gesture" in file_name)):
        #df = pd.read_csv(f'{current_directory}/data/whole_dataset_{file_name}')
        df = pd.read_csv(f'{current_directory}/data/{file_name}')
        right_edge = 0
        left_edge = 0
        counter = 0
        while(right_edge < df.shape[0]):
            # cut if left or right hand is invalid
            if((df["L_is_valid"][right_edge] == False) or (df["R_is_valid"][right_edge] == False)):
                name = file_name.replace(".csv", "---" + str(counter) + ".csv")
                name = name.replace("whole_dataset_","")
                df[left_edge:right_edge].to_csv(path + "/" + name)
                counter = counter + 1
                left_edge = right_edge
            right_edge = right_edge + 1

    #bei right_hand gesture einfach dort cutten wo right hand invalid ist
    if("right_hand" in file_name):
        #df = pd.read_csv(f'{current_directory}/data/whole_dataset_{file_name}')
        df = pd.read_csv(f'{current_directory}/data/{file_name}')
        right_edge = 0
        left_edge = 0
        counter = 0
        while(right_edge < df.shape[0]):
            # cut if right hand is invalid
            if(df["R_is_valid"][right_edge] == False):
                name = file_name.replace(".csv", "---" + str(counter) + ".csv")
                name = name.replace("whole_dataset_","")
                df[left_edge:right_edge].to_csv(path + "/" + name)
                counter = counter + 1
                left_edge = right_edge
            right_edge = right_edge + 1


def load_data_from_csv(file_name):
    df = pd.read_csv(f'data/{file_name}')
    df.drop(df.filter(regex="Unname"), axis=1, inplace=True)
    return df

#save_data_to_csv("60_times_right_hand_right_swipe_gesture_2022-05-24-10-19-32.bag")
#extract_single_movements("whole_dataset_60_times_right_hand_right_swipe_gesture_2022-05-24-10-19-32.csv")

current_directory = os.getcwd() + "/src/iviz_msgs"
print(pd.read_csv(current_directory + "/data/whole_dataset_60_times_right_hand_right_swipe_gesture_2022-05-24-10-19-32.csv"))
