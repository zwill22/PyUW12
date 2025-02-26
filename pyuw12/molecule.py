import os

from pyscf.gto import Mole
from pyuw12.printer import printVal
from pathvalidate import is_valid_filepath


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
        x = float(coords[1])
        y = float(coords[2])
        z = float(coords[3])

        atoms.append(symbol)
        coord = (x, y, z)
        coordinates.append(coord)

    return xyz_string(atoms, coordinates)


def check_molecule(mol: Mole):
    """
    Check the molecule setup

    Args:
        mol (Mole): PySCF molecule

    Raises:
        ValueError: Empty molecule
    """
    if mol.natm == 0:
        raise ValueError("No molecule specified")


def printMoleculeDetails(mol: Mole, verbosity: int = 1, **kwargs):
    """
    Print molecule details for verbosity level

    Args:
        mol (Mole): PySCF molecule
        verbosity (int, optional): Verbosity level. Defaults to 1.
    """
    if verbosity < 1:
        return
    print("Molecule")
    print(mol.atom)
    print()
    printVal("Basis set", mol.basis.upper())
    printVal("Number of atoms", mol.natm)
    printVal("Number of electrons", mol.nelectron)
    printVal("Number of basis functions", mol.nao)
    printVal("Charge", mol.charge)
    printVal("Total spin", mol.spin)
    printVal("Multiplicity", mol.multiplicity)
    print()
    printVal("Nuclear energy", "{:.6f}".format(mol.enuc))


def setupMol(atom: str, **kwargs) -> Mole:
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

    if is_valid_filepath(atom, platform="auto"):
        print("File path: {}".format(atom))
        if not os.path.isfile(atom):
            raise FileNotFoundError("Cannot find file: {}".format(atom))
        molecule = read_xyz(atom)
    else:
        molecule = atom

    mol = Mole(atom=molecule, **kwargs)
    mol.build()

    check_molecule(mol)

    printMoleculeDetails(mol, **kwargs)

    return mol



if __name__ == "__main__":
    project_dir = os.path.dirname(os.path.abspath(__file__))
    water = os.path.abspath(os.path.join(project_dir, "..", "molecules", "co2.xyz"))
    mol = setupMol(water, charge=2)
