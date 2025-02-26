import os

from pyscf.scf import RHF, UHF, RKS, UKS

from pyuw12 import setupMol
from pyuw12.printer import printVal

B3LYP_WITH_VWN5 = True

def checkMethod(xc, restricted, **kwargs) -> str:
    if xc.upper() == "HF":
        if restricted:
            printVal("Method", "Restricted Hartree-Fock", **kwargs)
        else:
            printVal("Method", "Unrestricted Hartree-Fock", **kwargs)
    else:
        if restricted:
            printVal("Method", "Restricted Kohn-Sham DFT", **kwargs)
        else:
            printVal("Method", "Unrestricted Kohn-Sham DFT", **kwargs)
        printVal("XC Functional", xc.upper(), **kwargs)


def getSCF(mol, xc="lda,vwn", restricted=True, **kwargs):
    checkMethod(xc, restricted, **kwargs)

    if xc.upper() == "HF":
        if restricted:
            return RHF(mol)
        else:
            return UHF(mol)
    else:
        if restricted:
            scf = RKS(mol)
        else:
            scf = UKS(mol)

        scf.xc = xc

        return scf


if __name__ == "__main__":
    project_dir = os.path.dirname(os.path.abspath(__file__))
    water = os.path.abspath(os.path.join(project_dir, "..", "molecules", "h2o.xyz"))
    mol = setupMol(atom=water, verbose=1)

    for xc in ("HF", "lda,vwn", "b88,lyp", "b3lyp5"):
        for restricted in (True, False):
            scf = getSCF(mol, xc=xc, restricted=restricted)

            e_tot = scf.kernel()
            printVal("SCF Energy", "{:.10f}".format(e_tot))
            print()
