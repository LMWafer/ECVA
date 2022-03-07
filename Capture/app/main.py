import os
import time
import cv2                  # state of the art computer vision algorithms library
import json as js           # JSON encoder and decoder
import shutil as shu
import numpy as np          # fundamental package for scientific computing
import pyrealsense2 as rs   # Intel RealSense cross-platform open-source API
from threading import Lock



img = cv2.Mat(np.zeros((1, 1)))
previous_timestamp = -1.0
image_ready = False
lock = Lock()

#-() Callback function called by pipeline when started
def imu_callback(frame: rs.frame) -> None:
    global previous_timestamp, image_ready, img
    #-> If lock already in use - during frame usage - blocks this statement, otherwise blocks other statements
    with lock:
        #-> Convert to frameset
        frameset = frame.as_frameset()
        if frameset:
            #-> Retrieve timestamp and ignore identical frameset based on their timestamp
            current_timestamp = frameset.get_timestamp()
            if abs(previous_timestamp - current_timestamp) < 0.001:
                return
                
            #-> If frameset is new, retrieve its color frame and convert it to opencv Mat
            color_frame = frameset.get_color_frame()
            img = np.asanyarray(color_frame.get_data())
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            #-> Convert timestamp from milliseconds to seconds
            previous_timestamp = frameset.timestamp * 1e-3

            #-> Turn on the flag for available image
            image_ready = True


def record() -> tuple:
    global previous_timestamp, image_ready, img
    #-> Setup
    pipe = rs.pipeline()
    cfg = rs.config()
    cfg.enable_stream(rs.stream.color, format=rs.format.any, width=1280, height=720, framerate=30)
    pipe.start(cfg, imu_callback)

    #-> Skip first frames to give the Auto-Exposure time to adjust
    time.sleep(1)

    frames = []
    timestamps = []
    while True:
        #-> If lock already in use - during frame retrieval - blocks this statement, otherwise blocks other statements
        with lock:
            if image_ready:
                timestamp = previous_timestamp
                frame = img.copy()
                image_ready = False

                timestamps.append(timestamp)
                frames.append(frame)

                cv2.imshow("Frame", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

    #-> Cleanup
    pipe.stop()
    return frames, timestamps


def saveJson(frames: list, timestamps: list) -> None:
    #-> Path setup
    bus_path = "/Bus"
    root_path = os.path.join(bus_path, "data")
    save_path = os.path.join(root_path, "sample/sample1")

    if "data" in os.listdir(bus_path):
        shu.rmtree(save_path)
    os.makedirs(os.path.join(save_path, "color"), exist_ok=True)

    #-> Camera device setup
    pipe = rs.pipeline()
    cfg = rs.config()
    cfg.enable_stream(rs.stream.color)

    #-> Intrinsics retrieval
    profile = pipe.start(cfg)
    intrinsics = profile.get_stream(
        rs.stream.color).as_video_stream_profile().get_intrinsics()
    intrinsics = [[intrinsics.fx, 0,             intrinsics.ppx],
                  [0,             intrinsics.fy, intrinsics.ppy],
                  [0,             0,             1]]
    
    #-> Cleanup
    pipe.stop()

    frames_info = []
    for i in range(len(frames)):
        #-> Prepare data : paths and fill frames info
        number = "0" * (8-len(str(i))) + str(i)
        frame_path = os.path.join(save_path, "color", number + ".jpg")
        frame_info = {"file_name_image": frame_path,
                      "timestamp": timestamps[i],
                      "intrinsics": intrinsics}

        #-> Save frames
        frames_info.append(frame_info)
        cv2.imshow("frame captured", frames[i])
        cv2.imwrite(frame_path, frames[i])
        if cv2.waitKey(10) & 0xFF == ord("q"):
            break
    
    #-> Save frames info file
    info = {"dataset": "sample",
            "path": "/Bus/sample",
            "scene": "sample1",
            "frames": frames_info}
    info_path = os.path.join(save_path, "info.json")
    js.dump(info, open(info_path, "w"))


if __name__ == "__main__":
    saveJson(*record())
