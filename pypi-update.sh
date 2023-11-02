#!/bin/bash
set -e

OS=`uname`

if [ "$OS" = "Darwin" ]
then
    python3 ../Py2C/bin/nuitka-watch --python-version=3.10 --nuitka-binary=../Nuitka-develop/bin/nuitka
    python3 ../Py2C/bin/nuitka-watch --python-version=3.11 --nuitka-binary=../Nuitka-develop/bin/nuitka
else
    python3.10 ../Py2C/bin/nuitka-watch --python-version=3.10 --nuitka-binary=../Nuitka-develop/bin/nuitka
fi
