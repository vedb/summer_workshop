"""
Created on Tue Jun 22 08:18:22 2021

Usage: mp_detect_faces(video_path, save_path, start_index, end_index)

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

@author: KamranBinaee
"""

import cv2
import mediapipe as mp
import math
import sys
import os

def mp_detect_faces(video_path, save_path, start_index = 0, end_index = 900):

    start_index = int(start_index)
    end_index = int(end_index)
    
    # In case one wants to downsample the image for a faster code
    world_scale = 1
    if os.path.exists(video_path):
        cap = cv2.VideoCapture(video_path)
    else:
        print("video_file does not exist! {}".format(video_path))
        return False
    fourcc = 'mp4v'
    output_video_file = save_path +"/detected_face.mp4"
    total_frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print("total frame count: {}".format(total_frame_count))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * world_scale)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * world_scale)
    video_size = (frame_width, frame_height)
    fps = 30
    print("output video file: ", output_video_file)
    out_video = cv2.VideoWriter(output_video_file,cv2.VideoWriter_fourcc(*fourcc), fps, video_size)


    # In  the first argument should be 'cv2.cv.CV_CAP_PROP_POS_FRAMES' without any magic '1' or '2'. The second one is the frame number in range 0 - cv2.cv.CV_CAP_PROP_FRAME_COUNT 
    # cap = cv2.VideoCapture(0)
    print("Start: {} and End Frames: {}".format(start_index, end_index))
        
    mp_drawing = mp.solutions.drawing_utils
    mp_face_mesh = mp.solutions.face_mesh

    count = start_index
    # Confidence values below are critical in determining how many false detection will be there in the output

    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    # cap = cv2.VideoCapture(0)
    with mp_face_mesh.FaceMesh(min_detection_confidence=0.1,min_tracking_confidence=0.1) as face_mesh:
        while cap.isOpened():
            cap.set(cv2.cv2.CAP_PROP_POS_FRAMES, count)
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                break

            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # cv2.flip(image, 1)
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            results = face_mesh.process(image)

            # Draw the face mesh annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACE_CONNECTIONS,
                        landmark_drawing_spec=drawing_spec,
                        connection_drawing_spec=drawing_spec)
            cv2.imshow('MediaPipe FaceMesh', cv2.resize(image, None, fx=0.5, fy=0.5))
            count +=1
            out_video.write(image)
            if cv2.waitKey(1) & 0xFF == 27:
                break
    cap.release()
    out_video.release()
    cv2.destroyAllWindows()
    print("Done!")
if __name__ == "__main__":
    video_path = sys.argv[1]
    save_path = sys.argv[2]
    start_index = sys.argv[3]
    end_index = sys.argv[4]
    print("args:", sys.argv)
    mp_detect_faces(video_path, save_path, start_index, end_index)
