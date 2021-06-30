"""
Created on Tue Jun 16 10:22:18 2020

Usage: python show_gaze_overlay.py [data_path] [start_time] [end_time]

        Parameters
        ----------
        start_index: int, len 1
            start index in the eye video

        end_time: int, len 1
            end index in the eye video

        data_path: str
            path to the data folder

@author: KamranBinaee

"""

# import the necessary libraries
import numpy as np
import cv2
import imageio
import matplotlib.pyplot as plt
import sys
import argparse
import os
import pandas as pd
import mediapipe as mp
import math

def read_input_arguments(args):

    # World video is recorded at 30 fps
    fps = 30
    # read the input arguments and store them to start and end time
    start_time = tuple(args.start_time)
    end_time = tuple(args.end_time)
    print('Start Time:', start_time)
    print('End Time:', end_time)

    start_index = (start_time[0] * 60 + start_time[1]) * fps
    end_index = (end_time[0] * 60 + end_time[1]) * fps
    print('Start Frame idx = %d' % start_index)
    print('End Frame idx= %d' % end_index)

    data_path = args.data_path[0]
    print('reading video: ', data_path + '/eye0.mp4')

    return start_index, end_index, data_path


def add_text_to_image(image, text):
    # font
    font = cv2.FONT_HERSHEY_SIMPLEX
    # org
    org = (1600, 200)
    # fontScale
    font_scale = 3
    # Blue color in BGR
    color = (0, 255, 255)
    # Line thickness of 2 px
    thickness = 3
#     text = "confidence: " + str(np.round(gaze_data_frame.confidence.values[gaze_index], 3))
    # Using cv2.putText() method
    image = cv2.putText(
    image, text, org, font, font_scale, color, thickness, cv2.LINE_AA
    )
    return image

def detect_draw_checkerboard(gray, img):
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (6,8),None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        #print('====> Found [%d]!' %(count))

        corners = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        # Draw and display the corners
    return img, ret, corners



def show_gaze_overlay(data_path, start_index, end_index):
    horizontal_pixels = 1280
    vertical_pixels = 1024

    scale_x = 0.5
    scale_y = 0.5

    # Todo: Pass fps as an argument
    fps = 30

    #gaze_data_frame = pd.read_csv(fpath + 'exports' + sub_folder + 'gaze_positions.csv')
    gaze_data_frame = pd.read_csv(data_path + '/gaze_positions.csv')
    world_time_stamps = np.load(data_path + '/world_timestamps.npy')

    camera = 'world'
    vid = imageio.get_reader(data_path + '/world.mp4',  'ffmpeg')
    cap = cv2.VideoCapture(data_path + '/world.mp4')

    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    size = (frame_width, frame_height)
    print('frame size:', size)
    #start_index = (start[0] * 60 + start[1]) * fps
    #end_index = (end[0] * 60 + end[1]) * fps
    print('First Frame = %d' % start_index)
    print('Last Frame = %d' % end_index)

    print('scale[x,y] = ', scale_x, scale_y)

    # Instantiate the video recorder in order to store the processed images to an output video
    size = (int(horizontal_pixels*scale_x), int(vertical_pixels*scale_y))
    print(size)
    fourcc = 'mp4v'
    out = cv2.VideoWriter('annotated_video.mp4',cv2.VideoWriter_fourcc(*fourcc), 30, size)
    # out_fovea = cv2.VideoWriter('fovea_output.mp4',cv2.VideoWriter_fourcc(*fourcc), 30, (100,100))
    # Read the next frame from the video.
    for i in range(start_index, end_index):

        #img = imstack[i,:,:,:]
        img = vid.get_data(i)
        img[:, :, [0, 2]] = img[:, :, [2, 0]]
        img = cv2.resize(img, None, fx=scale_x, fy=scale_y)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        img, ret, corners = detect_draw_checkerboard(gray, img)
        if ret == True:
            img = cv2.drawChessboardCorners(img, (6,8), corners,ret)

        gaze_index = np.argmin(
            np.abs((gaze_data_frame.gaze_timestamp.values - world_time_stamps[i]).astype(float)))
        gaze_norm_x = gaze_data_frame.norm_pos_x.values[gaze_index]
        gaze_norm_y = gaze_data_frame.norm_pos_y.values[gaze_index]

        gaze_pixel_x = int(gaze_norm_x * horizontal_pixels * scale_x)
        gaze_pixel_y = int((1 - gaze_norm_y) * vertical_pixels * scale_y)
        frame_no_gaze = img.copy()
        img = cv2.circle(img, (gaze_pixel_x, gaze_pixel_y), 10, (255,255,0), 8)

        # Todo: Create a separate function for adding text info on the frame
        # font
        font = cv2.FONT_HERSHEY_SIMPLEX
        # org
        org = (10, 30)
        # fontScale
        font_scale = 0.5
        # Blue color in BGR
        color = (0, 255, 255)
        # Line thickness of 2 px
        thickness = 1
        text = 'confidence: ' + str(np.round(gaze_data_frame.confidence.values[gaze_index], 2))
        # Using cv2.putText() method
        img = cv2.putText(img, text, org, font,
                            font_scale, color, thickness, cv2.LINE_AA)

        w = 50
        h = 50
        x_min = gaze_pixel_x - w
        x_max = gaze_pixel_x + w

        y_min = gaze_pixel_y - h
        y_max = gaze_pixel_y + h

        if gaze_pixel_x-w <0:
            x_min = 0
            x_max = 2*w
        if gaze_pixel_x+w >= (horizontal_pixels * scale_x):
            x_min = horizontal_pixels * scale_x - 2*w - 1
            x_max = horizontal_pixels * scale_x - 1

        if gaze_pixel_y-h <0:
            y_min = 0
            y_max = 2*h
        if gaze_pixel_y+h >= (vertical_pixels * scale_y):
            y_min = vertical_pixels * scale_y - 2*h - 1
            y_max = vertical_pixels * scale_y - 1

        range_x = np.arange(int(x_min), int(x_max))
        range_y = np.arange(int(y_min), int(y_max))

        fovea = frame_no_gaze[int(y_min):int(y_max), int(x_min):int(x_max), :]
        # print(frame_no_gaze.shape, fovea.shape)
        #print(range_x.shape, range_y.shape)
        #print(range_x.min(), range_x.max(), range_y.min(), range_y.max())
        cv2.imshow('img', img)
        out.write(img)
        # cv2.imshow('fovea', fovea)
        # out_fovea.write(fovea)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print('\nDone!')

    cv2.destroyAllWindows()
    # Release the video writer handler so that the output video is saved to disk
    out.release()
    # out_fovea.release()


if __name__ == "__main__":
    data_path = sys.argv[1]
    start_index = int(sys.argv[2])
    end_index = int(sys.argv[3])
    print("args:", sys.argv)
    show_gaze_overlay(data_path, start_index, end_index)
