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

typedef py::array_t<double> PyArray;

auto setupMats(
    const PyArray & X3_np,
    const PyArray & X2_np
) {
    const arma::mat X3_mat = carma::arr_to_mat<double>(X3_np);
    const arma::mat X2_mat = carma::arr_to_mat<double>(X2_np);

    const auto N = X3_mat.n_rows;
    const auto n_ao = static_cast<size_t>((std::sqrt(8*N + 1) + 1) / 2);
    assert(N == (n_ao * (n_ao + 1) / 2));

    const auto n_df = X2_mat.n_rows;

    assert(X3_mat.n_cols == n_df);
    assert(X2_mat.n_cols == n_df);
    assert(X2_mat.n_cols == n_df);

    return std::pair(X3_mat, X2_mat);
}

uw12::BaseIntegrals setupBaseIntegrals(
    const PyArray & X3_np,
    const PyArray & X2_np
) {
    const auto &[X3_mat, X2_mat] = setupMats(X3_np, X2_np);

    return uw12::BaseIntegrals(X3_mat, X2_mat);
}

uw12::BaseIntegrals setupBaseIntegrals(
    const PyArray & X3_np,
    const PyArray & X2_np,
    const PyArray & X3_ri_np
) {
    const auto &[X3_mat, X2_mat] = setupMats(X3_np, X2_np);
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

    return uw12::BaseIntegrals(X3_mat, X2_mat, X3_ri_mat);
}

uw12::ABSProjectors setupABSProjectors(
    const PyArray &S,
    const size_t n_ao,
    const size_t n_ri
) {
    assert(S.ndim() == 2);
    const auto n0 = S.shape(0);
    const auto n1 = S.shape(1);

    assert(n0 == n_ao + n_ri);
    assert(n1 == n0);

    return uw12::setup_abs_projectors(S.data(), n_ao, n_ri);
}

uw12::Orbitals setupOrbitals(const PyArray & C) {
    if (C.ndim() != 3) {
        throw std::runtime_error("Array is of invalid size");
    }

    const auto n_spin = C.shape(0);
    if (n_spin > 2) {
        throw std::runtime_error("Invalid number of spin channels");
    }
    const auto n_ao = C.shape(1);
    const auto n_orb = C.shape(2);

    return uw12::setup_orbitals(C.data(), n_ao, n_orb, n_spin);
}

// TODO Fix this for varied occupations
uw12::Occupations setupOccupations(const PyArray & occ) {
    if (occ.ndim() != 2) {
        throw std::runtime_error("Occupations array is of invalid size");
    }

    const auto n_ao = occ.shape(1);
    const auto n_orb = occ.shape(2);

    const auto n_spin = occ.shape(0);
    if (n_spin == 1) {
        return uw12::setup_occupations(occ.data(), n_orb);
    } else if (n_spin == 2) {
        return uw12::setup_occupations(occ.data(), n_orb, n_orb);
    } else {
        throw std::runtime_error("Invalid number of spin channels");
    }
}

/// @brief Calculate the UW12 energy from the provided integrals
///
/// @param W3  Three-index integrals \f$(\rho\sigma | w_{12} | A)\f$
/// @param W2  Two-index integrals \f$(A | w_{12} | B)\f$
/// @param W3_ri Three-index RI integrals \f$(\mu\rho|w_{12}|A)\f$
/// @param V3 Three-index integrals \f$(\rho\sigma | r_{12}^{-1} | A)\f$
/// @param V2 Two-index integrals \f$(A | r_{12}^{-1} | B)\f$
/// @param V3_ri Three-index RI integrals \f$(\mu\rho|r_{12}^{-1}|A)\f$
/// @param WV3 Three-index integrals \f$(\rho\sigma | w_{12} r_{12}^{-1} | A)\f$
/// @param WV2 Two-index integrals \f$(A | w_{12} r_{12}^{-1} | B)\f$
/// @param S Overlap Matrix \f$(\mu | \nu)\f$ for combined AO+RI space
/// @param C Orbital coefficients for each spin channel
/// @param occ Occupation vectors for each spin channel
/// @param n_active Number of active orbitals in each spin channel
/// @param scale_opp_spin Scale factor for osUW12
/// @param scale_same_spin Scale factor for ssUW12
/// @param print_level Adjust print details (0-3), default:0 (silent)
///
/// @return The UW12 correlation energy
double uw12_energy(
    const PyArray & W3,
    const PyArray & W2,
    const PyArray & W3_ri,
    const PyArray & V3,
    const PyArray & V2,
    const PyArray & V3_ri,
    const PyArray & WV3,
    const PyArray & WV2,
    const PyArray & S,
    const PyArray & C,
    const PyArray & occ,
    const py::list & n_active,
    const double scale_opp_spin,
    const double scale_same_spin,
    const size_t print_level
) {
    const auto n_ao = C.shape(0);
    const auto n_df = W2.shape(0);
    const auto n_ri = S.shape(0) - n_ao;

    assert(W3.ndim() == 2);
    assert(W2.ndim() == 2);
    assert(W3_ri.ndim() == 2);

    assert(V3.ndim() == 2);
    assert(V2.ndim() == 2);
    assert(V3_ri.ndim() == 2);

    assert(WV3.ndim() == 2);
    assert(WV2.ndim() == 2);

    assert(W3.shape(0) == n_ao * (n_ao + 1) / 2);
    assert(W3.shape(1) == n_df);
    assert(W2.shape(0) == n_df);
    assert(W2.shape(1) == n_df);
    assert(W3_ri.shape(0) == n_ao * n_ri);
    assert(W3_ri.shape(1) == n_df);

    assert(V2.shape(0) == n_ao * (n_ao + 1) / 2);
    assert(V3.shape(1) == n_df);
    assert(V2.shape(0) == n_df);
    assert(V2.shape(1) == n_df);
    assert(V3_ri.shape(0) == n_ao * n_ri);
    assert(V3_ri.shape(1) == n_df);

    assert(WV3.shape(0) == n_ao * (n_ao + 1) / 2);
    assert(WV3.shape(1) == n_df);
    assert(WV2.shape(0) == n_df);
    assert(WV2.shape(1) == n_df);
    
    const auto W = setupBaseIntegrals(W3, W2, W3_ri);
    const auto V = setupBaseIntegrals(V3, V2, V3_ri);
    const auto WV = setupBaseIntegrals(WV3, WV2);

    assert(S.ndim() == 2);
    assert(S.shape(1) == n_ao + n_ri);

    const auto abs_proj = setupABSProjectors(S, n_ao, n_ri);

    const auto orbitals = setupOrbitals(C);
    const auto occupations = setupOccupations(occ);

    const auto n_active_orb = n_active.cast<std::vector<size_t>>();

    uw12::uw12_energy(W, V, WV, abs_proj, orbitals, occupations, n_active_orb, scale_opp_spin, scale_same_spin, print_level);
}

/// @brief Pybind Module interface
///
/// @param Interface name
/// @param Interface label
PYBIND11_MODULE(uw12_interface, m) {
    m.doc() = "Pybind plugin for libuw12";

    m.def("uw12_energy", &uw12interface::uw12_energy, "A function that calculates the UW12 energy");
}
