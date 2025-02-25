import pytest
import numpy as np
from pyscf import gto, scf
from numpy.linalg import LinAlgError


def test_empty_molecule():
    mol = gto.Mole()

    mol.build()

    assert mol.atom == []
    assert mol.basis == "sto-3g"
    assert mol.cart is False
    assert mol.charge == 0
    assert mol.ecp == {}
    assert mol.elements == []
    assert mol.enuc == 0
    assert mol.groupname == "C1"
    assert mol.incore_anyway is False
    assert mol.irrep_id is None
    assert mol.irrep_name is None
    assert mol.magmom == []
    assert mol.max_memory == 4000
    assert mol.ms == 0
    assert mol.multiplicity == 1
    assert mol.nao == 0
    assert mol.natm == 0
    assert mol.nbas == 0
    assert mol.nelec == (0, 0)
    assert mol.nelectron == 0
    assert mol.nucmod == {}
    assert mol.nucprop == {}
    assert mol.output is None
    assert mol.pseudo is None
    assert mol.spin == 0
    assert mol.symm_orb is None
    assert mol.symmetry is False
    assert mol.symmetry_subgroup is None
    assert mol.topgroup == "C1"
    assert mol.unit == "angstrom"
    assert mol.verbose == 3

    myscf = scf.RHF(mol)
    assert myscf.callback is None
    assert myscf.check_convergence is None
    assert myscf.conv_check is True
    assert myscf.conv_tol == 1e-9
    assert myscf.conv_tol_cpscf == 1e-8
    assert myscf.conv_tol_grad is None
    assert myscf.converged is False
    assert myscf.cycles == 0
    assert myscf.damp == 0
    assert myscf.diis is True
    assert myscf.diis_damp == 0
    assert myscf.diis_file is None
    assert myscf.diis_space == 8
    assert myscf.diis_space_rollback == 0
    assert myscf.diis_start_cycle == 1
    assert myscf.direct_scf is True
    assert myscf.direct_scf_tol == 1e-13
    assert myscf.disp is None
    assert myscf.e_tot == 0
    assert myscf.init_guess == "minao"
    assert myscf.level_shift == 0
    assert myscf.max_cycle == 50
    assert myscf.max_memory == 4000
    assert myscf.mo_coeff is None
    assert myscf.mo_energy is None
    assert myscf.mo_occ is None
    assert myscf.mol == mol
    assert myscf.opt is None
    assert myscf.sap_basis == "sapgrasplarge"
    assert myscf.scf_summary == {}
    assert myscf.verbose == 3

    with pytest.raises(LinAlgError):
        myscf.kernel()


def test_atom():
    mol = gto.Mole()

    mol.build(atom="O")

    assert mol.atom == "O"
    assert mol.basis == "sto-3g"
    assert mol.cart is False
    assert mol.charge == 0
    assert mol.ecp == {}
    assert mol.elements == ["O"]
    assert mol.enuc == 0
    assert mol.groupname == "C1"
    assert mol.incore_anyway is False
    assert mol.irrep_id is None
    assert mol.irrep_name is None
    assert mol.magmom == [0]
    assert mol.max_memory == 4000
    assert mol.ms == 0
    assert mol.multiplicity == 1
    assert mol.nao == 5
    assert mol.natm == 1
    assert mol.nbas == 3
    assert mol.nelec == (4, 4)
    assert mol.nelectron == 8
    assert mol.nucmod == {}
    assert mol.nucprop == {}
    assert mol.output is None
    assert mol.pseudo is None
    assert mol.spin == 0
    assert mol.symm_orb is None
    assert mol.symmetry is False
    assert mol.symmetry_subgroup is None
    assert mol.topgroup == "C1"
    assert mol.unit == "angstrom"
    assert mol.verbose == 3

    myscf = scf.RHF(mol)
    assert myscf.callback is None
    assert myscf.check_convergence is None
    assert myscf.conv_check is True
    assert myscf.conv_tol == 1e-9
    assert myscf.conv_tol_cpscf == 1e-8
    assert myscf.conv_tol_grad is None
    assert myscf.converged is False
    assert myscf.cycles == 0
    assert myscf.damp == 0
    assert myscf.diis is True
    assert myscf.diis_damp == 0
    assert myscf.diis_file is None
    assert myscf.diis_space == 8
    assert myscf.diis_space_rollback == 0
    assert myscf.diis_start_cycle == 1
    assert myscf.direct_scf is True
    assert myscf.direct_scf_tol == 1e-13
    assert myscf.disp is None
    assert myscf.e_tot == 0
    assert myscf.init_guess == "minao"
    assert myscf.level_shift == 0
    assert myscf.max_cycle == 50
    assert myscf.max_memory == 4000
    assert myscf.mo_coeff is None
    assert myscf.mo_energy is None
    assert myscf.mo_occ is None
    assert myscf.mol == mol
    assert myscf.opt is None
    assert myscf.sap_basis == "sapgrasplarge"
    assert myscf.scf_summary == {}
    assert myscf.verbose == 3

    e_hf = myscf.kernel()
    assert e_hf == np.float64(-73.66181689790079)


def test_molecule():
    mol = gto.Mole()
    water = """
    O
    H  1  1.2
    H  1  1.2  2 105
    """
    mol.atom = water

    mol.build()
    print(mol.atom)
    assert mol.atom == water
    assert mol.basis == "sto-3g"
    assert mol.cart is False
    assert mol.charge == 0
    assert mol.ecp == {}
    assert mol.elements == ["O", "H", "H"]
    assert mol.enuc == np.float64(7.333618344136481)
    assert mol.groupname == "C1"
    assert mol.incore_anyway is False
    assert mol.irrep_id is None
    assert mol.irrep_name is None
    assert mol.magmom == [0, 0, 0]
    assert mol.max_memory == 4000
    assert mol.ms == 0
    assert mol.multiplicity == 1
    assert mol.nao == 7
    assert mol.natm == 3
    assert mol.nbas == 5
    assert mol.nelec == (5, 5)
    assert mol.nelectron == 10
    assert mol.nucmod == {}
    assert mol.nucprop == {}
    assert mol.output is None
    assert mol.pseudo is None
    assert mol.spin == 0
    assert mol.symm_orb is None
    assert mol.symmetry is False
    assert mol.symmetry_subgroup is None
    assert mol.topgroup == "C1"
    assert mol.unit == "angstrom"
    assert mol.verbose == 3

    myscf = scf.RHF(mol)
    assert myscf.callback is None
    assert myscf.check_convergence is None
    assert myscf.conv_check is True
    assert myscf.conv_tol == 1e-9
    assert myscf.conv_tol_cpscf == 1e-8
    assert myscf.conv_tol_grad is None
    assert myscf.converged is False
    assert myscf.cycles == 0
    assert myscf.damp == 0
    assert myscf.diis is True
    assert myscf.diis_damp == 0
    assert myscf.diis_file is None
    assert myscf.diis_space == 8
    assert myscf.diis_space_rollback == 0
    assert myscf.diis_start_cycle == 1
    assert myscf.direct_scf is True
    assert myscf.direct_scf_tol == 1e-13
    assert myscf.disp is None
    assert myscf.e_tot == 0
    assert myscf.init_guess == "minao"
    assert myscf.level_shift == 0
    assert myscf.max_cycle == 50
    assert myscf.max_memory == 4000
    assert myscf.mo_coeff is None
    assert myscf.mo_energy is None
    assert myscf.mo_occ is None
    assert myscf.mol == mol
    assert myscf.opt is None
    assert myscf.sap_basis == "sapgrasplarge"
    assert myscf.scf_summary == {}
    assert myscf.verbose == 3

    e_hf = myscf.kernel()
    assert e_hf == np.float64(-74.89488697720347)
