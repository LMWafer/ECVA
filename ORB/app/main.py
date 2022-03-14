import json
import numpy as np
from scipy.spatial.transform import Rotation as rot

info_path = "/Bus/data/sample/sample1/info.json"
info = json.load(open(info_path))
frames = info["frames"]
timestamps = [float(frame["timestamp"])*10e8 for frame in frames]

with open("CameraTrajectory.txt", "r") as input_file:
    lines = list(map(lambda line: line[:-1:], input_file.readlines()))
    for i in range(len(lines)):
        line = lines[i].split(" ")
        
        timestamp, tx, ty, tz, qx, qy, qz, qw = float(line[0][:19:]), *map(float, line[1:])
        # print(datetime.datetime.fromtimestamp(timestamp / 10e9))
        translation_matrix = np.array([[tx, ty, tz]])
        rotation = rot.from_quat([qx, qy, qz, qw])

        # roration_matrix = rotation.as_matrix()
        # rot_trans_matrix = np.concatenate((roration_matrix, translation_matrix.T), axis=1)
        # filling_matrix = np.array([[0, 0, 0, 1]])
        # extrinsics_matrix = np.concatenate((rot_trans_matrix, filling_matrix), axis=0)

        extrinsics_matrix = np.block([
            [rotation.as_matrix(),  translation_matrix.T], 
            [np.zeros((1, 3)),      np.array([[1]])]
        ])
        # print(extrinsics_matrix, end="\n\n")
        # index = timestamps.index(min(timestamps, key=lambda x:abs(x-timestamp)))
        frames[timestamps.index(timestamp)]["pose"] = extrinsics_matrix.tolist()

info["frames"] = [frame for frame in frames if "pose" in frame.keys()]


json.dump(info, open(info_path, "w"), indent=4)