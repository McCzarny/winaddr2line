cmake_minimum_required(VERSION 3.15)
project(TestApp CXX)

add_executable(test_app src/testApp.cpp)

target_compile_options(test_app PRIVATE /Zi /Od) 

# Tell linker to include symbol data
set_target_properties(test_app PROPERTIES 
    LINK_FLAGS "/INCREMENTAL:NO /DEBUG /OPT:REF /OPT:ICF"
)

# Set file name & location
set_target_properties(test_app PROPERTIES 
    COMPILE_PDB_NAME test_app
    COMPILE_PDB_OUTPUT_DIR ${CMAKE_BINARY_DIR}
)

