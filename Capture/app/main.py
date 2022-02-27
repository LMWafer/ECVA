import cv2                                # state of the art computer vision algorithms library
import numpy as np                        # fundamental package for scientific computing
import pyrealsense2 as rs                 # Intel RealSense cross-platform open-source API

#-> Setup
pipe = rs.pipeline()
cfg = rs.config()
cfg.enable_stream(rs.stream.color)
profile = pipe.start(cfg)

#-> Skip 5 first frames to give the Auto-Exposure time to adjust
for _ in range(5):
  pipe.wait_for_frames()

while True:
  #-> Retrieve frame set
  #-? A frameset is a packet with 1 frame from each enabled stream (depth, color, gyro, accel)
  frameset = pipe.wait_for_frames()
  
  #-> Get color frame from framset
  color_frame = frameset.get_color_frame()

  #-> Get the actual frame that is the frame data
  #-? You can get a lot of thing from a frame : metadata, data size, timestamp etc.
  frame = np.asanyarray(color_frame.get_data())

  #-> Swap RED and BLUE channels
  #-? Intel returns BGR, opencv uses RGB by default
  frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  cv2.imshow("frame.png", frame)

  #-> Window closure handler
  if cv2.waitKey(10) & 0xFF == ord("q"):
        break

#-> Cleanup
pipe.stop()
