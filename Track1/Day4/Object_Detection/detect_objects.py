"""
Created on Thr Jun 18 14:52:11 2021

Usage: python detect_objects.py [video_path] [model_path] [start_time] [end_time] [show_output]

        Parameters
        ----------

        start_index: int, len 1
            start index in the eye video

        end_time: int, len 1
            end index in the eye video

        video_path: str
            path to the video

        model_path: str
            path to the data folder
         
        show_output: bool
            show the output during runtime

@author: KamranBinaee
"""

import cv2
import numpy as np
import argparse
import os
import sys


def detect_objects(video_path, model_path, start_index, end_index, show_output=False):

    if (video_path == 'webcam'):
        print('reading from: webcam')
        cap = cv2.VideoCapture(0)
    else:
        print('reading from: ', video_path)
        cap = cv2.VideoCapture(video_path)
    cap.set(3, 640) #WIDTH
    cap.set(4, 512) #HEIGHT

    fps = cap.get(cv2.CAP_PROP_FPS)
    print('FPS: ', fps)
    video_size = (640, 512)
    fourcc = 'XVID'
    out_video = cv2.VideoWriter('detected_objects_output.avi',cv2.VideoWriter_fourcc(*fourcc), fps, video_size)

    # Load Yolo
    net = cv2.dnn.readNet(model_path + "/yolov3.weights", model_path + "/yolov3.cfg")
    classes = []
    with open(model_path + "/coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    # Creating a text file to save the class titles
    text_file = open('detected_objects.txt',"w") 

    minimum_probability = 0.5

    frame_count = start_index
    while(cap.isOpened()):
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Loading image
        #img = cv2.imread("room_ser.jpg")

        img = cv2.resize(img, None, fx=0.5, fy=0.5)
        height, width, channels = img.shape
        #print(height, width, channels)

        # Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > minimum_probability:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
                    # Save the bouding box position and size to csv

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        #print(indexes)
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[i]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 30), font, 1.5, color, 3)
                # \n is placed to indicate EOL (End of Line) 
                text_file.writelines(label + ',' +  str(x) + ',' + 
                                    str(y) + ',' + str(w) + ',' + 
                                    str(h) + ',' + str(frame_count) + '\n')

        out_video.write(img)
        if(show_output):
            cv2.imshow("Image", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        frame_count =+ 1
        if frame_count > end_index:
            break
    text_file.close()
    out_video.release()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print("args:", sys.argv)
    video_path = sys.argv[1]
    model_path = sys.argv[2]
    start_index = int(sys.argv[3])
    end_index = int(sys.argv[4])
    if len(sys.argv)>5:
        show_output = bool(sys.argv[5])
    else:
        show_output = False
    detect_objects(video_path, model_path, start_index, end_index, show_output)

