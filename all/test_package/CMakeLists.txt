cmake_minimum_required(VERSION 3.6.1)
project(test_package)

find_package(openpnp-capture CONFIG REQUIRED)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} openpnp-capture::openpnp-capture)
