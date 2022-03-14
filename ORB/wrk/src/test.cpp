#include <iostream>
#include <fstream>
#include "json.hpp"

using json = nlohmann::json;
using namespace std;

int main() {
    ofstream output_file ("test.json", ofstream::out);
    vector<float> frame_pose ({1.f, 2.f, 3.f, 4.f, 5.f, 6.f, 7.f, 8.f, 9.f, 10.f, 11.f, 12.f});
    json j = json::parse(frame_pose.begin(), frame_pose.end());
    for (int i = 0; i < frame_pose.size(); i ++) {
        cout << frame_pose[i] << endl;
    }
    // json j = json::parse(frame_pose.begin(), frame_pose.end());
    // output_file << setw(4) << j << std::endl;
    output_file.close();
    return EXIT_SUCCESS;
}