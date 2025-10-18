#!/bin/bash

set -e
shopt -s expand_aliases

OS=`uname`
echo "Running on $OS..."
if [[ $OS = MINGW* ]]
then
    python3.10() {
        '/c/Python310_64/python.exe' $@
    }
    python3.11() {
        '/c/Python311_64/python.exe' $@
    }
    python3.12() {
        '/c/Python312_64/python.exe' $@
    }
    python3.13() {
        '/c/Python313_64/python.exe' $@
    }
fi

# This enables my private development slightly better.
if [ -d "../Py2C" ]
then
    # Self compiled Pythons over system pythons.
    PATH=/opt/self-built-pythons/bin/:$PATH

    NUITKA_WATCH="../Py2C"
    if [ "$OS" = "Linux" ]
    then
        . fake-x11-display.sh || true
    fi
else
    NUITKA_WATCH="../Nuitka-factory"
fi

if [ "$OS" = "Darwin" ]
then
    declare -a PYTHON_VERSIONS=("3.10" "3.11" "3.12")
elif [ "$OS" = "Linux" ]
then
    declare -a PYTHON_VERSIONS=("3.10" "3.11" "3.12" "3.13")
else
    declare -a PYTHON_VERSIONS=("3.10" "3.12" "3.13")
fi

echo "Doing Python versions $PYTHON_VERSIONS"

for PYTHON_VERSION in "${PYTHON_VERSIONS[@]}"
do
    python${PYTHON_VERSION} $NUITKA_WATCH/bin/nuitka-watch --python-version=${PYTHON_VERSION} --nuitka-binary=../Nuitka-develop/bin/nuitka $@
done
