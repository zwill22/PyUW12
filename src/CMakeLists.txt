set(PYBIND11_NEWPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(uw12_interface main.cpp)

target_link_libraries(uw12_interface PRIVATE uw12 carma::carma)
target_include_directories(uw12_interface PRIVATE ${libuw12_SOURCE_DIR} ${libuw12_SOURCE_DIR}/src ${PyUW12Backend_BINARY_DIR}/src)

install(TARGETS uw12_interface DESTINATION pyuw12_backend)
