import os
import glob
import numpy as np
import cv2
# from matplotlib import pyplot as plt

frames_path = "/Bus/data/sample/sample1/color"
frames = [cv2.imread(os.path.join(frames_path, frame)) for frame in sorted(os.listdir(frames_path))]

# Initiate ORB detector
orb = cv2.ORB_create()

for frame in frames:
    # find the keypoints with ORB
    kp = orb.detect(frame, None)
    # compute the descriptors with ORB
    kp, des = orb.compute(frame, kp)
    # draw only keypoints location,not size and orientation
    frame2 = cv2.drawKeypoints(frame, kp, None, color=(0, 255, 0), flags=0)
    cv2.imshow("frame", frame2)

    cv2.waitKey(60)