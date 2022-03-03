#include <iostream>
// #include <iomanip>
#include <fstream>
#include <opencv2/opencv.hpp>
#include <System.h>
#include "json.hpp"


using json = nlohmann::json;
using namespace std;

int main()
{
    //-[] Load the JSON data
    ifstream file ("info.json", ifstream::in);
    string line;
    string content;
    if (file.is_open())
    {
        while (getline(file, line)) {
            content.append(line + "\n");
        }
        file.close();
    }
    else
        cout << "Unable to open file";
    json j = json::parse(content);
    auto frames (j["frames"]);
    cout << frames.size() << "frames found" << endl;

    //-> Initialisze SLAM system object, get its map handler and image scale required
    string path_to_vocabulary = "ORBvoc.txt";
    string path_to_settings = "RealSense_D435i.yaml";
    string previous_File_Name;
    ORB_SLAM3::System SLAM(path_to_vocabulary, path_to_settings, ORB_SLAM3::System::MONOCULAR, true, 0, previous_File_Name);
    // auto atlas = SLAM.mpAtlas;
    // std::vector<MapPoint *> map;
    float imageScale = SLAM.GetImageScale();

    for (int i = 0; i < frames.size(); i++)
    {
        //-> Retrieve the image and its timestamp
        cv::Mat frame(cv::imread(frames[i]["file_name_image"]));
        float timestamp = frames[i]["timestamp"];

        cout << "Timestamp " << i << " " << timestamp << endl;
        
        //-> Rescale the image
        if (imageScale != 1.f)
        {
            int width = frame.cols * imageScale;
            int height = frame.rows * imageScale;
            cv::resize(frame, frame, cv::Size(width, height));
        }

        //-> Feed the SLAM with the frame
        SLAM.TrackMonocular(frame, timestamp);

        // cv::imshow("frame", frame);
        cv::waitKey(60);
    }

    SLAM.SaveTrajectoryEuRoC("CameraTrajectory.txt");
    SLAM.Shutdown();
    cout << "System shutdown!\n";
    return EXIT_SUCCESS;
}