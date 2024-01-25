"""
PyUW12 main interface. This program functions as a wrapper for PySCF whereby
any PySCF function may be used in addition to UW12 calculations
"""

from pyscf import gto, dft


def main():
    # Setup molecule
    mol = gto.Mole()
    mol.atom = '''O 0 0 0; H  0 1 0; H 0 0 1'''
    mol.basis = 'sto-3g'
    mol.symmetry = False
    mol.charge = 0
    mol.spin = 0
    mol.verbose = 4
    mol.max_memory = 1000
    mol.build()

    mf_hf = dft.RKS(mol)
    mf_hf.xc = "lda,vwn"
    mf_hf.kernel()

    return 0


if __name__ == '__main__':
    main()
