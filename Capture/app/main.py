import os                   # miscellaneous operating system interfaces
import cv2                  # state of the art computer vision algorithms library
import json as js           # JSON encoder and decoder
import shutil as shu
from cv2 import imshow        # high level file opertions
import numpy as np          # fundamental package for scientific computing
import pyrealsense2 as rs   # Intel RealSense cross-platform open-source API

# -> Setup
bus_path = "/Bus"
root_path = os.path.join(bus_path, "data")
save_path = os.path.join(root_path, "sample/sample1")

if "data" in os.listdir(bus_path):
    shu.rmtree(root_path)
os.makedirs(os.path.join(save_path, "color"), exist_ok=True)


def record():
    pipe = rs.pipeline()
    cfg = rs.config()
    cfg.enable_stream(rs.stream.color, format=rs.format.any, width=640, height=480, framerate=60)
    pipe.start(cfg)

    # -> Skip 5 first frames to give the Auto-Exposure time to adjust
    for _ in range(5):
        pipe.wait_for_frames()

    frames = []
    timestamps = []
    while True:
        # -> Retrieve frame set
        # -? A frameset is a packet with 1 frame from each enabled stream (depth, color, gyro, accel)
        frameset = pipe.wait_for_frames()

        # -> Get color frame from framset
        color_frame = frameset.get_color_frame()

        # -> Get the actual frame that is the frame data
        # -? You can get a lot of thing from a frame : metadata, data size, timestamp etc.
        frame = np.asanyarray(color_frame.get_data())
        timestamp = color_frame.get_timestamp()

        # -> Swap RED and BLUE channels
        # -? Intel returns BGR, opencv uses RGB by default
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frames.append(frame)
        timestamps.append(timestamp)

        cv2.imshow("frame.png", frame)

        # -> Window closure handler
        if cv2.waitKey(10) & 0xFF == ord("q"):
            break
    
    pipe.stop()
    return frames, timestamps


def saveJson(frames, timestamps):
    pipe = rs.pipeline()
    cfg = rs.config()
    cfg.enable_stream(rs.stream.color)
    profile = pipe.start(cfg)
    intrinsics = profile.get_stream(
        rs.stream.color).as_video_stream_profile().get_intrinsics()
    intrinsics = [[intrinsics.fx, 0,             intrinsics.ppx],
                  [0,             intrinsics.fy, intrinsics.ppy],
                  [0,             0,             1]]
    pipe.stop()

    frames_info = []
    for i in range(len(frames)):
        # -> Prepare data : paths and fill frame info
        number = "0" * (8-len(str(i))) + str(i)
        frame_path = os.path.join(save_path, "color", number + ".jpg")
        frame_info = {"file_name_image": frame_path,
                      "timestamp": timestamps[i],
                      "intrinsics": intrinsics}

        # -> Save data
        frames_info.append(frame_info)
        imshow("frame captured", frames[i])
        cv2.imwrite(frame_path, frames[i])
        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

    info = {"dataset": "sample",
            "path": "/Bus/sample",
            "scene": "sample1",
            "frames": frames_info}
    info_path = os.path.join(save_path, "info.json")
    js.dump(info, open(info_path, "w"))

if __name__ == "__main__":
    saveJson(*record())
