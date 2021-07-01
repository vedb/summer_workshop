<<<<<<< Updated upstream:Track2/Day4/Hand_Detection/mp_detect_hands.py
"""
Created on Tue Jun 22 08:18:22 2021

Usage: mp_detect_bodies(video_path, save_path, start_index, end_index, show_output)

        Parameters
        ----------

        video_path: str
            path to the video

        save_path: str
            path to the saving directory

        start_index: int
            start index of the video

        end_index: int
            end index of the video
        
        show_output: bool
            show the output during runtime
@author: KamranBinaee
"""
=======
# %load mp_detect_hands.py
>>>>>>> Stashed changes:Track2/Day4/Hand_Detection/hand_utils.py

import cv2
import mediapipe as mp
import math
import sys
import os


def __getEuclideanDistance(posA, posB):
    return math.sqrt((posA.x - posB.x)**2 + (posA.y - posB.y)**2)

def __isThumbNearIndexFinger(thumbPos, indexPos):
    return __getEuclideanDistance(thumbPos, indexPos) < 0.1

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

def simpleGesture(handLandmarks):
    """Guess gesture from configuration of fingers"""
    thumbIsOpen = False
    indexIsOpen = False
    middelIsOpen = False
    ringIsOpen = False
    pinkyIsOpen = False
    text = ""

    pseudoFixKeyPoint = handLandmarks[2].x
    if handLandmarks[3].x < pseudoFixKeyPoint and handLandmarks[4].x < pseudoFixKeyPoint:
        thumbIsOpen = True

    pseudoFixKeyPoint = handLandmarks[6].y
    if handLandmarks[7].y < pseudoFixKeyPoint and handLandmarks[8].y < pseudoFixKeyPoint:
        indexIsOpen = True

    pseudoFixKeyPoint = handLandmarks[10].y
    if handLandmarks[11].y < pseudoFixKeyPoint and handLandmarks[12].y < pseudoFixKeyPoint:
        middelIsOpen = True

    pseudoFixKeyPoint = handLandmarks[14].y
    if handLandmarks[15].y < pseudoFixKeyPoint and handLandmarks[16].y < pseudoFixKeyPoint:
        ringIsOpen = True

    pseudoFixKeyPoint = handLandmarks[18].y
    if handLandmarks[19].y < pseudoFixKeyPoint and handLandmarks[20].y < pseudoFixKeyPoint:
        pinkyIsOpen = True

    if thumbIsOpen and indexIsOpen and middelIsOpen and ringIsOpen and pinkyIsOpen:
        print("\r FIVE!", end = "\r")
        text = "FIVE!"

    elif not thumbIsOpen and indexIsOpen and middelIsOpen and ringIsOpen and pinkyIsOpen:
        print("\r FOUR!", end = "\r")
        text = "FOUR!"

    elif not thumbIsOpen and indexIsOpen and middelIsOpen and ringIsOpen and not pinkyIsOpen:
        print("\r THREE!", end = "\r")
        text = "THREE!"

    elif not thumbIsOpen and indexIsOpen and middelIsOpen and not ringIsOpen and not pinkyIsOpen:
        print("\r TWO!", end = "\r")
        text = "TWO!"

    elif not thumbIsOpen and indexIsOpen and not middelIsOpen and not ringIsOpen and not pinkyIsOpen:
        print("\r ONE!", end = "\r")
        text = "ONE!"

    elif not thumbIsOpen and indexIsOpen and not middelIsOpen and not ringIsOpen and pinkyIsOpen:
        print("\r ROCK!", end = "\r")
        text = "ROCK!"

    elif thumbIsOpen and indexIsOpen and not middelIsOpen and not ringIsOpen and pinkyIsOpen:
        print("\r SPIDERMAN!", end = "\r")
        text = "SPIDERMAN!"

    elif not thumbIsOpen and not indexIsOpen and not middelIsOpen and not ringIsOpen and not pinkyIsOpen:
        print("\r PALM!", end = "\r")
        text = "PALM!"

    elif not indexIsOpen and middelIsOpen and ringIsOpen and pinkyIsOpen and __isThumbNearIndexFinger(handLandmarks[4], handLandmarks[8]):
        print("\r OK!", end = "\r")
        text = "OK!"

    return text
#     print("FingerState: thumbIsOpen? " + str(thumbIsOpen) + " - indexIsOpen? " + str(indexIsOpen) + " - middelIsOpen? " +
#        str(middelIsOpen) + " - ringIsOpen? " + str(ringIsOpen) + " - pinkyIsOpen? " + str(pinkyIsOpen))

def mp_detect_hands(video_path, save_path, start_index = 0, end_index = 900, save_video=False):
    """Detect hands in a clip of a video

    Parameters
    ----------
    video_path: str
        path to the video
    save_path: str
        path to the saving directory
    start_index: int
        start index of the video
    end_index: int
        end index of the video
    save_video: bool (optional, default False)
        flag to save an output video or not

    @author: KamranBinaee
    """
    # Outputs
    gestures = np.zeros((end_index-start_index,))
    locations = []
    landmarks = []
    # Inputs
    start_index = int(start_index)
    end_index = int(end_index)
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    # In case one wants to downsample the image for a faster code
    world_scale = 0.5
    if os.path.exists(video_path):
        cap = cv2.VideoCapture(video_path)
    else:
        print("video_file does not exist! {}".format(video_path))
        return False
    total_frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print("total frame count: {}".format(total_frame_count))
    if save_video:
        fourcc = 'mp4v'
        output_video_file = save_path +"/detected_hand.mp4"
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * world_scale)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * world_scale)
        video_size = (frame_width, frame_height)
        fps = 30
        print("output video file: ", output_video_file)
        out_video = cv2.VideoWriter(output_video_file,cv2.VideoWriter_fourcc(*fourcc), fps, video_size)

    print("Start: {} and End Frames: {}".format(start_index, end_index))
        
    count = start_index

    # for webcam video stream
    #cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        cap.set(cv2.cv2.CAP_PROP_POS_FRAMES, start_index)
        while cap.isOpened() and count < end_index:
            cap.set(cv2.cv2.CAP_PROP_POS_FRAMES, count)
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                break
            image = cv2.resize(image, None, fx=world_scale, fy=world_scale)
            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # cv2.flip(image, 1)
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            results = hands.process(image)
            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                xyzpos_frame = []
                action_id_frame = []
                landmarks_frame = []
                
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    action_id = simpleGesture(hand_landmarks.landmark)
                    if save_video:
                        add_text_to_image(image, action_id)
                    xyzpos = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark])
                    x, y, z = xyzpos.mean(0)
                    xyzpos_frame.append([x,y,z])
                    action_id_frame.append(action_id)
                    landmark_frame.append(hand_landmarks)
            else:
            #cv2.imshow('MediaPipe Hands', cv2.resize(image, None, fx=0.5, fy=0.5))
            count +=1
            if save_video:
                out_video.write(image)
            #if cv2.waitKey(1) & 0xFF == 27:
            #    break
    cap.release()
    if save_video:
        out_video.release()
    #cv2.destroyAllWindows()
    return result_list
