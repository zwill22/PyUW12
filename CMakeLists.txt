cmake_minimum_required(VERSION 3.12)
message(STATUS "CMake ${CMAKE_VERSION}")

project(pyuw12 LANGUAGES CXX VERSION 0.1)

find_package(Python 3 COMPONENTS Interpreter Development)

message(STATUS "Python_FOUND: ${Python_FOUND}")
message(STATUS "Python_VERSION: ${Python_VERSION}")
message(STATUS "Python_LIBRARIES: ${Python_LIBRARIES}")
message(STATUS "Python_EXECUTABLE: ${Python_EXECUTABLE}")
message(STATUS "Python_INCLUDE_DIRS: ${Python_INCLUDE_DIRS}")

if (NOT ${Python_FOUND})
    message(FATAL_ERROR "Python interpreter not found")
endif ()

add_subdirectory(external)
