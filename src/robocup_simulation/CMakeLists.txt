cmake_minimum_required(VERSION 3.8)
project(robocup_simulation)
find_package(ament_cmake REQUIRED)
install(DIRECTORY launch worlds urdf models config rviz
  DESTINATION share/${PROJECT_NAME})
install(PROGRAMS scripts/trajectory_demo.py
  DESTINATION lib/${PROJECT_NAME})
ament_package()
