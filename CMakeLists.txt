cmake_minimum_required(VERSION 3.15)
project(winaddr2line CXX)

set (CMAKE_CXX_STANDARD 17)

add_executable(${PROJECT_NAME} src/main.cpp src/DbgHelpManager.cpp)

target_include_directories(${PROJECT_NAME} PUBLIC include)

target_link_libraries(${PROJECT_NAME} PRIVATE Dbghelp)

install(TARGETS ${PROJECT_NAME}  RUNTIME LIBRARY RUNTIME)

add_subdirectory(testing_binary)

enable_testing()

add_test(
    NAME run_tests
    COMMAND python3 ./test/test.py $<TARGET_FILE:winaddr2line>
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
)