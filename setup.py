#!/usr/bin/env python2.7

from setuptools import setup

VERSION = '0.1.1'

setup(name='b2blaze',
      version=VERSION,
      description='b2blaze library for connecting to Backblaze B2',
      packages=['b2blaze'],
      author='George Sibble',
      author_email='gsibble@gmail.com',
      python_requires='==2.7',
      url='https://github.com/sibblegp/b2blaze',
      install_requires=[
            'requests==2.19.1'
      ],
      keywords='backblaze b2 cloud storage',
      classifiers=[
            'Programming Language :: Python :: 2.7',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries',
      ],
      license='MIT'
)
