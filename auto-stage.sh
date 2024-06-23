#!/bin/bash

set -e
shopt -s expand_aliases

OS=`uname`
echo "Running on $OS..."
if [[ $OS = MINGW* ]]
then
    alias python3='/c/Python310_64/python.exe'
fi

# This enables my private development slightly better.
if [ -d "../Py2C" ]
then
    NUITKA_WATCH="../Py2C"
else
    NUITKA_WATCH="../Nuitka-factory"
fi

PYTHONPATH=$NUITKA_WATCH python3 $NUITKA_WATCH/nuitka/tools/watch/AutoStage.py
