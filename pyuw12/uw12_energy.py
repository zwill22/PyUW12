import os

from pyscf import df, gto
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

    df_basis = "ccpvdz-jk-fit"
    ri_basis = "ccpvdz-fit"

    df_mol = df.addons.make_auxmol(mol, df_basis)
    ri_mol = mol.copy()
    ri_mol.basis = "cc-pVDZ-F12-OptRI"
    ri_mol.build(False, False)

    mol_full = gto.conc_mol(mol, ri_mol)
    s = mol_full.intor_symmetric("int1e_ovlp")
    obs = (0, mol.nbas)
    abs = (mol.nbas, mol_full.nbas)
    dfbs = (0, df_mol.nbas)
    shls_slice = obs + abs + dfbs

    # (ij|P) n_ao * n_ao * n_df
    V3 = df.incore.aux_e2(mol, df_mol, "int3c2e")
    # (P|Q) n_df * n_df
    V2 = df_mol.intor("int2c2e")
    # (i\mu | P)
    V3_ri = df.incore.aux_e2(mol_full, df_mol, "int3c2e", shls_slice=obs + abs + dfbs)
