//
// Created by Zack Williams on 24/01/2024.
//

#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace uw12 {

    int uw12_energy(int i, int j) {

        return i + j;
    }

}

PYBIND11_MODULE(uw12_interface, m) {
    m.doc() = "Pybind plugin";

    m.def("uw12_energy", &uw12::uw12_energy, "A function that adds two numbers");
}
