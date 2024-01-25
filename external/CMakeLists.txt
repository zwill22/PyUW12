cmake_minimum_required(VERSION 3.12)

if (DEFINED uw12_interface_MASTER_PROJECT)
    return()
endif()

project(uw12_library_interface LANGUAGES CXX VERSION 0.1)

# Check if pybind11 is being used directly
if(CMAKE_SOURCE_DIR STREQUAL PROJECT_SOURCE_DIR)
  message(STATUS "Building uw12_interface")

  # Warn if an out-of-source build
  if(CMAKE_CURRENT_SOURCE_DIR STREQUAL CMAKE_CURRENT_BINARY_DIR)
    message(STATUS "CMAKE_CURRENT_BINARY_DIR: ${CMAKE_CURRENT_BINARY_DIR}")
  else()
    set(AUTHOR_WARNING "You are build uw12_interface out of place,"
    "Python may not find resulting library")
  endif()
  set(uw12_interface_MASTER_PROJECT ON)
# Or using add_subdirectory
else()
  set(uw12_interface_MASTER_PROJECT OFF)
endif()

find_package(pybind11 REQUIRED)

pybind11_add_module(uw12_interface uw12_interface.cpp)
