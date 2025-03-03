//
// Created by Zack Williams on 24/01/2024.
//

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#include <armadillo>
#include <carma>

#include "libuw12.hpp"

#include <pybind11/numpy.h>

namespace py = pybind11;

namespace uw12interface {


uw12::BaseIntegrals setupBaseIntegrals(
    const py::array_t<double> & X3_np,
    const py::array_t<double> & X2_np,
    const py::array_t<double> & X3_ri_np
) {
    const arma::mat X3_mat = carma::arr_to_mat<double>(X3_np);
    const arma::mat X2_mat = carma::arr_to_mat<double>(X2_np);
    const arma::mat X3_ri_mat = carma::arr_to_mat<double>(X3_ri_np);

    const auto N = X3_mat.n_rows;
    const auto n_ao = static_cast<size_t>((std::sqrt(8*N + 1) + 1) / 2);
    assert(N == (n_ao * (n_ao + 1) / 2));

    const auto n_df = X2_mat.n_rows;
    const auto n_ri = static_cast<size_t>(X3_ri_mat.n_rows / n_ao);

    assert(X3_mat.n_cols == n_df);
    assert(X2_mat.n_cols == n_df);
    assert(X2_mat.n_cols == n_df);

    assert(X3_ri_mat.n_rows == n_ao * n_ri);

    return uw12::setup_base_integrals(
        X3_mat.memptr(), X2_mat.memptr(), X3_ri_mat.memptr(), n_ao, n_df, n_ri, true);
}

/// @brief Example function
///
/// @param i An integer
/// @param j Another integer
///
/// @return The sum of i and j
int uw12_energy(int i, int j) {

    return i + j;
}

}

/// @brief Pybind Module interface
///
/// @param Interface name
/// @param Interface label
PYBIND11_MODULE(uw12_interface, m) {
    m.doc() = "Pybind plugin";

    m.def("uw12_energy", &uw12interface::uw12_energy, "A function that adds two numbers");
}
