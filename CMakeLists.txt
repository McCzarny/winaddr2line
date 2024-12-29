cmake_minimum_required(VERSION 3.15)
project(winaddr2line CXX)

set (CMAKE_CXX_STANDARD 17)

add_executable(winaddr2line src/main.cpp src/DbgHelpManager.cpp)

target_include_directories(winaddr2line PUBLIC include)

target_link_libraries(winaddr2line PRIVATE Dbghelp)
