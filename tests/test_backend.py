"""
Unit test to test pytest functions
"""

from pyuw12_backend import uw12_interface


def function():
    return 0


def test_function():
    assert function() == 0


def test_uw12_energy():
    assert uw12_interface.uw12_energy(1, 2) == 3
