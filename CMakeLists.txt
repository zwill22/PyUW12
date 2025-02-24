cmake_minimum_required(VERSION 3.22)
message(STATUS "CMake ${CMAKE_VERSION}")

project(PyUW12Backend LANGUAGES CXX VERSION 0.1.0)

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
find_package(pybind11 CONFIG REQUIRED)

add_subdirectory(src)
