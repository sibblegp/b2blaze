#!/bin/bash

echo Building and installing $(pwd)

echo "Clean build..."
/usr/bin/python3 setup.py clean --all && echo -e "OK\n"

echo "Build..."
/usr/bin/python3 setup.py build && echo -e "OK\n"

echo "Install" 
sudo -H /usr/bin/python3 setup.py install && echo -e "OK\n"

