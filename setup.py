from setuptools import setup, find_packages
with open('README.txt') as f:
    readme = f.read()

with open('LICENSE') as f:
    myLicense = f.read()

setup(
    name="PyUW12",
    version='0.1.0',
    description="",
    long_description=readme,
    author="Zack M. Williams",
    author_email="z.m.williams4@gmail.com",
    url="https://github.com/zwill22/pyuw12",
    packages=find_packages(exclude=('tests', 'docs'))
)