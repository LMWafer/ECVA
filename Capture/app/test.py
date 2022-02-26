import pyrealsense2 as rs
import cv2 as cv 

config = rs.config()
config.enable_stream(rs.stream.color)

pipe = rs.pipeline()
profile = pipe.start(config)
try:
  while True:
    frames = pipe.wait_for_frames()
    for f in frames:
      print(f.profile)
        # d = f.get_data()
        # cv.imshow("frame", d)
        # if cv.waitKey(10) & 0xFF == ord("q"):
            # break

      
finally:
    pipe.stop()