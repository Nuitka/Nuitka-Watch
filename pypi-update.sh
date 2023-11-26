#!/bin/bash
set -e
shopt -s expand_aliases

OS=`uname`
echo "Running on $OS..."
if [[ $OS = MINGW* ]]
then
    alias python3='/c/Python310_64/python.exe'
fi

if [ "$OS" = "Darwin" ]
then
    python3 ../Py2C/bin/nuitka-watch --python-version=3.10 --nuitka-binary=../Nuitka-develop/bin/nuitka $@
    python3 ../Py2C/bin/nuitka-watch --python-version=3.11 --nuitka-binary=../Nuitka-develop/bin/nuitka $@
else
    python3 ../Py2C/bin/nuitka-watch --python-version=3.10 --nuitka-binary=../Nuitka-develop/bin/nuitka $@
fi
