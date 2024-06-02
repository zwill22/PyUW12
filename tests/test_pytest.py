"""
Unit test to test pytest functions
"""

import package_pyuw12


def function():
    return 0


def test_function():
    assert function() == 0


def test_uw12_energy():
    assert package_pyuw12.uw12_energy(1, 2) == 3
