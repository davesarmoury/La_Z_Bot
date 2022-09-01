cmake_minimum_required(VERSION 3.0.2)
project(la_z_bot_description)

find_package(catkin REQUIRED COMPONENTS)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES la_z_bot_description
#  CATKIN_DEPENDS bunker_description realsense2_description xacro
#  DEPENDS system_lib
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)
