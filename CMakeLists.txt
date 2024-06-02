cmake_minimum_required(VERSION 3.12)
message(STATUS "CMake ${CMAKE_VERSION}")

project(package_pyuw12 LANGUAGES CXX VERSION 0.1)

# Find the module development requirements (requires FindPython from 3.17 or
# scikit-build-core's built-in backport)
find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
find_package(pybind11 CONFIG REQUIRED)

add_subdirectory(src)
