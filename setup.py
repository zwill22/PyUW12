import os.path

from glob import glob
from setuptools import setup, find_packages

from pybind11.setup_helpers import Pybind11Extension

name = "PyUW12"
description = "A Python package for UW12 calculations"
author = "Zack M. Williams"
author_email = "z.m.williams4@gmail.com"
url = "https://github.com/zwill22/pyuw12"
requires_python = ">=3.11.0"
version = "0.1.0"

with open('requirements.txt') as f:
    requirements = f.readlines()

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    myLicense = f.read()

setup_location = os.path.abspath(os.path.dirname(__file__))

ext_modules = [
    Pybind11Extension(
        "uw12_interface",
        sorted(glob("external/*.cpp"))
    ),
]

setup(
    name=name,
    version=version,
    description=description,
    long_description=readme,
    author=author,
    author_email=author_email,
    url=url,
    ext_modules=ext_modules,
    packages=find_packages(exclude=('tests', 'external', 'docs')),
    install_requires=requirements
)
