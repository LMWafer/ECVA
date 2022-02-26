cmake_minimum_required(VERSION 3.10.2)
project(app)

IF(NOT CMAKE_BUILD_TYPE)
  SET(CMAKE_BUILD_TYPE Release)
ENDIF()

MESSAGE("Build type: " ${CMAKE_BUILD_TYPE})

add_executable(${PROJECT_NAME} src/main.cpp)

#-> Look for dependencies
#-? This will fill <package>_INCLUDE_DIR and <package>_LIBRARY
find_package(OpenCV)
find_package(realsense2)

# If RealSense SDK is found the library is added and its examples compiled
if(realsense2_FOUND)
    include_directories(${PROJECT_NAME} ${realsense_INCLUDE_DIR})
    target_link_libraries(${PROJECT_NAME} ${realsense2_LIBRARY})
endif()

#-> Looks for .so files
#-? .so are shared object, no matter their position : they contains all the library features needed
#-? Function signatures are located in the lib include directory
target_link_libraries(${PROJECT_NAME}
${OpenCV_LIBS} 
# -lboost_serialization
# -lcrypto
)

install(TARGETS ${PROJECT_NAME} DESTINATION /app/)