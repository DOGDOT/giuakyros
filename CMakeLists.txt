cmake_minimum_required(VERSION 3.8)
project(assem3)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(urdf REQUIRED)
find_package(gazebo_ros REQUIRED)
find_package(robot_state_publisher REQUIRED)

# Đóng gói tất cả các thư mục quan trọng vào hệ thống
install(DIRECTORY 
  config 
  launch 
  meshes 
  rviz 
  scripts 
  urdf 
  worlds
  DESTINATION share/${PROJECT_NAME}
)
install(PROGRAMS 
  scripts/arm_node.py
  scripts/arm_teleop_key.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()