import os
import pyscf
import pathvalidate
import numpy as np


def xyz_string(atoms: list, coordinates: list) -> str:
    """
    Generate a string of XYZ coordinates that can be read by PySCF

    Args:
        atoms (list): List of atom symbols
        coordinates (list): List (x, y, z) coordinates as tuples

    Returns:
        str: XYZ format string
    """
    n = len(atoms)
    assert len(coordinates) == n

    output = ""
    for i in range(n):
        output += atoms[i]
        for coord in coordinates[i]:
            output += "\t"
            output += str(coord)
        output += "\n"

    return output


def read_xyz(filename) -> str:
    """
    Read an XYZ file from file `filename` and return the 
    contents in the form of a string that can be read by PySCF

    Args:
        filename: A file descriptor that can be open by `open`

    Raises:
        ValueError: If the XYZ file is not properly formatted

    Returns:
        str: XYZ contents as a string
    """
    atoms = []
    coordinates = []
    n = 0
    with open(filename, "r") as f:
        n = int(f.readline())
        _ = f.readline()
        result = f.readlines()

    if len(result) != n:
        raise ValueError("Invalid XYZ format")
    for atom in result:
        coords = atom.split()
        if len(coords) != 4:
            raise ValueError("Invalid XYZ format")
        symbol = coords[0].strip()
        x = np.float64(coords[1])
        y = np.float64(coords[2])
        z = np.float64(coords[3])

        atoms.append(symbol)
        coord = (x, y, z)
        coordinates.append(coord)

    return xyz_string(atoms, coordinates)


def setupMol(atom: str, **kwargs) -> pyscf.gto.Mole:
    """
    Setup and build a PySCF molecule. If `atom` is provided as a
    filepath, it is converted to a string that can be read by PySCF
    otherwise, the value is passed directly to PySCF

    Args:
        atom (str): String defining the atoms/molecule

    Raises:
        FileNotFoundError: If filepath is provided and cannot be found
        ValueError: If the final molecule is empty

    Returns:
        pyscf.gto.Mole: PySCF molecule
    """

    if pathvalidate.is_valid_filepath(atom, platform="auto"):
        print("File path: {}".format(atom))
        if not os.path.isfile(atom):
            raise FileNotFoundError("Cannot find file: {}".format(atom))
        molecule = read_xyz(atom)
    else:
        molecule = atom

    mol = pyscf.gto.Mole(atom=molecule, **kwargs)
    mol.build()

    if mol.natm == 0:
        raise ValueError("No molecule specified")

    return mol


def printVal(text: str, value, **kwargs):
    """
    Print a formatted value

    Args:
        text (str): Value name
        value: Value 
    """
    print("{0:<32} {1}".format(text, value), **kwargs)


if __name__ == "__main__":
    try:
        setupMol()
        raise RuntimeError("No exception thrown")
    except ValueError:
        pass

    project_dir = os.path.dirname(os.path.abspath(__file__))
    water = os.path.abspath(os.path.join(project_dir, "..", "molecules", "water.xyz"))
    mol = setupMol(atom=water, verbose=2)

    print("Molecule")
    print(mol.atom)
    print()
    printVal("Basis set", mol.basis.upper())
    printVal("Number of atoms", mol.natm)
    printVal("Number of electrons", mol.nelectron)
    printVal("Number of basis functions", mol.nao)
    printVal("Charge", mol.charge)
    printVal("Multiplicity", mol.multiplicity)
    print()
    printVal("Nuclear energy", "{:.6f}".format(mol.enuc))
    print("Running SCF...")

    scf = pyscf.scf.RHF(mol)

    result = scf.run()
    if not result.converged:
        print("SCF failed to converged after {} cycles".format(result.cycles))
        quit(0)

    print("SCF converged after {} cycles".format(result.cycles))
    print()
    printVal("E(HF)", "{:.10f}".format(result.e_tot))
