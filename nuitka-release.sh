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
    PATH=/opt/self-built-pythons/bin/:$PATH
    NUITKA_WATCH="../Py2C"
    . fake-x11-display.sh || true
else
    NUITKA_WATCH="../Nuitka-factory"
fi

if [ "$OS" = "Darwin" ]
then
    declare -a PYTHON_VERSIONS=("3.10" "3.11")
elif [ "$OS" = "Linux" ]
then
    declare -a PYTHON_VERSIONS=("3.10" "3.11" "3.12")
else
    declare -a PYTHON_VERSIONS=("3.10")
fi

echo "Doing Python versions $PYTHON_VERSIONS"

for PYTHON_VERSION in "${PYTHON_VERSIONS[@]}"
do
    python${PYTHON_VERSION} $NUITKA_WATCH/bin/nuitka-watch --python-version=${PYTHON_VERSION} --no-pipenv-update --nuitka-binary=../Nuitka-develop/bin/nuitka $@
done
