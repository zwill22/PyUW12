set(PYBIND11_NEWPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(uw12_interface main.cpp)

install(TARGETS uw12_interface DESTINATION package_pyuw12)
