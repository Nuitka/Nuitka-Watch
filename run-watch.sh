#!/bin/bash

set -e
shopt -s expand_aliases

OS=`uname`
echo "Running on $OS..."
if [[ $OS = MINGW* ]]
then
    if ! command -v python3.10 &> /dev/null; then
        if [ -f "/c/Python310_64/python.exe" ]; then
            python3.10() {
                '/c/Python310_64/python.exe' "$@"
            }
        elif [ -f "$LOCALAPPDATA/Programs/Python/Python310/python.exe" ]; then
            python3.10() {
                "$LOCALAPPDATA/Programs/Python/Python310/python.exe" "$@"
            }
        fi
    fi

    if ! command -v python3.11 &> /dev/null; then
        if [ -f "/c/Python311_64/python.exe" ]; then
            python3.11() {
                '/c/Python311_64/python.exe' "$@"
            }
        elif [ -f "$LOCALAPPDATA/Programs/Python/Python311/python.exe" ]; then
            python3.11() {
                "$LOCALAPPDATA/Programs/Python/Python311/python.exe" "$@"
            }
        fi
    fi

    if ! command -v python3.12 &> /dev/null; then
        if [ -f "/c/Python312_64/python.exe" ]; then
            python3.12() {
                '/c/Python312_64/python.exe' "$@"
            }
        elif [ -f "$LOCALAPPDATA/Programs/Python/Python312/python.exe" ]; then
            python3.12() {
                "$LOCALAPPDATA/Programs/Python/Python312/python.exe" "$@"
            }
        fi
    fi

    if ! command -v python3.13 &> /dev/null; then
        if [ -f "/c/Python313_64/python.exe" ]; then
            python3.13() {
                '/c/Python313_64/python.exe' "$@"
            }
        elif [ -f "$LOCALAPPDATA/Programs/Python/Python313/python.exe" ]; then
            python3.13() {
                "$LOCALAPPDATA/Programs/Python/Python313/python.exe" "$@"
            }
        fi
    fi

    if ! command -v python3.14 &> /dev/null; then
        if [ -f "/c/Python314_64/python.exe" ]; then
            python3.14() {
                '/c/Python314_64/python.exe' "$@"
            }
        elif [ -f "$LOCALAPPDATA/Programs/Python/Python314/python.exe" ]; then
            python3.14() {
                "$LOCALAPPDATA/Programs/Python/Python314/python.exe" "$@"
            }
        fi
    fi
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
    declare -a PYTHON_VERSIONS=("3.10" "3.11" "3.12" "3.14")
elif [ "$OS" = "Linux" ]
then
    declare -a PYTHON_VERSIONS=("3.10" "3.11" "3.12" "3.13" "3.14")
else
    declare -a PYTHON_VERSIONS=("3.10" "3.12" "3.13" "3.14")
fi

# Allow limiting to a single Python version via --python-version=X argument.
FILTERED_ARGS=()
SELECTED_PYTHON_VERSION=""
for arg in "$@"; do
    if [[ "$arg" == --python-version=* ]]; then
        SELECTED_PYTHON_VERSION="${arg#--python-version=}"
    else
        FILTERED_ARGS+=("$arg")
    fi
done

if [ -n "$SELECTED_PYTHON_VERSION" ]; then
    PYTHON_VERSIONS=("$SELECTED_PYTHON_VERSION")
fi

echo "Doing Python versions $PYTHON_VERSIONS"

for PYTHON_VERSION in "${PYTHON_VERSIONS[@]}"
do
    set -x
    # python${PYTHON_VERSION} $NUITKA_WATCH/bin/nuitka --clean-cache=all
    python${PYTHON_VERSION} $NUITKA_WATCH/bin/nuitka-watch --python-version=${PYTHON_VERSION} --nuitka-binary=../Nuitka-develop/bin/nuitka "${FILTERED_ARGS[@]}"
    set +x
done
