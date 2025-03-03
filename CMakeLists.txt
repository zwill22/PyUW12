cmake_minimum_required(VERSION 3.22)
project(PyUW12Backend LANGUAGES CXX VERSION 0.1.0)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

message(STATUS "Setting up PyUW12 backend...")
message(STATUS "CMake version: ${CMAKE_VERSION}")

# TODO Is Python necessary?
find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
message(STATUS "Found Python: ${Python_EXECUTABLE} (found version \"${Python_VERSION}\")")
find_package(pybind11 CONFIG REQUIRED)

include(FetchContent)
FetchContent_Declare(
  libuw12
  GIT_REPOSITORY https://github.com/zwill22/libuw12.git
  GIT_TAG        v0.1.1
  GIT_SHALLOW    TRUE
)

FetchContent_GetProperties(libuw12)
if(NOT libuw12_POPULATED)
  set(PARALLEL TBB)
  set(LINALG_LIB ARMA)
  set(USE_CATCH OFF)
endif()

FIND_PACKAGE(carma CONFIG REQUIRED)

message(STATUS "Setting up libuw12...")
FetchContent_MakeAvailable(libuw12)
message(STATUS "Setup libuw12 successfully")

add_subdirectory(src)
