import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="at-the-catastrophy-point",
    description="",
    author="Carl-Johan Rosén",
    packages=find_packages(exclude=['data', 'output']),
    long_description=read('README.md'),
)