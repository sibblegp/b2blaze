#!/usr/bin/env python2.7

from setuptools import setup, find_packages

VERSION = "0.2.1"

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()

setup(
    name="b2blaze",
    version=VERSION,
    description="Forked from George Sibble's B2Blaze (0.1.10). All credits to author. Original package: https://github.com/sibblegp/b2blaze",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    author="George Sibble",
    author_email="gsibble@gmail.com",
    python_requires=">=2.7",
    url="https://github.com/fieldse/b2blaze-fork",
    install_requires=["requests==2.19.1"],
    keywords="backblaze b2 cloud storage",
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
    license="MIT",
)
