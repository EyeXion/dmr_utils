#!/bin/bash

rm -rf build
mkdir build

cd build
sudo make uninstall
make clean
make
sudo make install
sudo ldconfig
