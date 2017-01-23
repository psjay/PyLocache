#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


def read_file(*path):
    base_dir = os.path.dirname(__file__)
    file_path = (base_dir, ) + tuple(path)
    return open(os.path.join(*file_path)).read()


setup(
    name="PyLocache",
    url="https://github.com/psjay/PyLocache",
    version="0.0.4",
    license='WTFPL',
    description="PyLocache is a Python implementation of LRU local cache.",
    long_description=(
        read_file("README.rst") + "\n\n" +
        "Change History\n" +
        "==============\n\n" +
        read_file("CHANGES.rst")),
    author='psjay',
    author_email="psjay.peng@gmail.com",
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
    install_requires=[],
    test_suite='nose.collector',
    setup_requires=['nose>=1.0'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)
