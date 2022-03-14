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
    ifstream input_file ("/Bus/data/sample/sample1/info.json", ifstream::in);
    string line;
    string content;
    json j;
    if (input_file.is_open()) {
        input_file >> j;
        input_file.close();
    }
    else
        cout << "Unable to open file";
    auto frames (j["frames"]);
    cout << frames.size() << " frames found" << endl;

    //-> Initialisze SLAM system object, get its map handler and image scale required
    string path_to_vocabulary = "ORBvoc.txt";
    string path_to_settings = "RealSense_D435i.yaml";
    string previous_File_Name;
    ORB_SLAM3::System SLAM(path_to_vocabulary, path_to_settings, ORB_SLAM3::System::MONOCULAR, true, 0, previous_File_Name);
    // auto atlas = SLAM.mpAtlas;
    // std::vector<MapPoint *> map;
    float imageScale = SLAM.GetImageScale();

    for (int i = 0; i < frames.size(); i++) {
        //-> Retrieve the image and its timestamp
        cv::Mat frame(cv::imread(frames[i]["file_name_image"]));
        auto timestamp = frames[i]["timestamp"];

        cout << "Timestamp " << i << " " << timestamp << endl;
        
        //-> Rescale the image
        if (imageScale != 1.f) {
            int width = frame.cols * imageScale;
            int height = frame.rows * imageScale;
            cv::resize(frame, frame, cv::Size(width, height));
        }

        //-> Feed the SLAM with the frame
        SLAM.TrackMonocular(frame, timestamp);
    }

    SLAM.SaveTrajectoryEuRoC("CameraTrajectory.txt");
    try {
        SLAM.Shutdown();
    }
    catch (exception& e ) {
        cout << "Expected segmentation fault, system shutdown sucessful ! ; )" << endl;
    }

    return EXIT_SUCCESS;
}