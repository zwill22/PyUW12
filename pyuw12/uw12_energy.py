import os

import pyscf
from pyuw12 import setupMol, getSCF
from pyuw12.printer import printVal

if __name__ == "__main__":
    project_dir = os.path.dirname(os.path.abspath(__file__))
    water = os.path.abspath(os.path.join(project_dir, "..", "molecules", "h2o.xyz"))
    mol = setupMol(atom=water, verbose=1, basis="cc-pvdz")

    scf = getSCF(mol, xc="b3lyp5", restricted=True)
    scf.run()

    printVal("E(B3LYP)", scf.e_tot)


    mo = scf.mo_coeff
    occ = scf.get_occ()
