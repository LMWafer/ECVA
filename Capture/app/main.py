import cv2 as cv
import sys

cam = cv.VideoCapture(-1)
if not cam.isOpened():
    sys.exit("Cannot open camera")

while True:
    ret, frame = cam.read()
    if not ret:
        sys.exit("Not frame found")
    
    # ... 
    cv.imshow("frame", frame)

    if cv.waitKey(10) & 0xFF == ord("q"):
        break
cam.release()