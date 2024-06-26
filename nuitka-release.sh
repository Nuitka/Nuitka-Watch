#!/bin/bash

set -e
shopt -s expand_aliases

OS=`uname`
echo "Running on $OS..."
if [[ $OS = MINGW* ]]
then
    alias python3.10='/c/Python310_64/python.exe'
    alias python3.11='/c/Python311_64/python.exe'
    alias python3.12='/c/Python312_64/python.exe'
fi

# This enables my private development slightly better.
if [ -d "../Py2C" ]
then
    NUITKA_WATCH="../Py2C"
else
    NUITKA_WATCH="../Nuitka-factory"
fi

if [ "$OS" = "Darwin" ]
then
    python3.10 $NUITKA_WATCH/bin/nuitka-watch --python-version=3.10 --no-pipenv-update --nuitka-binary=../Py2C/bin/nuitka $@
    python3.11 $NUITKA_WATCH/bin/nuitka-watch --python-version=3.11 --no-pipenv-update --nuitka-binary=../Nuitka-develop/bin/nuitka $@
else
    python3.10 $NUITKA_WATCH/bin/nuitka-watch --python-version=3.10 --no-pipenv-update --nuitka-binary=../Nuitka-develop/bin/nuitka $@
fi
