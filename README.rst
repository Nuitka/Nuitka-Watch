Nuitka Watch
============

This repository is under construction. The intention is to detect PyPI package
updates, and check if Nuitka is working with them.

One idea is to detect ``scipy`` breaking on a platform with Nuitka due to DLL
changes right away, and not have to wait until somebody reports it, and then
probably not in the correct fashion.

The other idea is to detect regressions inside the Nuitka plugin mechanisms
and standalone capabilities automatically.

And the important idea, is to do all of that in a distributed fashion, because
there is no way for one user to compile everything on all platforms for every
release of Nuitka and a PyPI package.

The ``nuitka-watch`` tool will scan for installed Pythons. Right now you are
expected to install the dependencies in this requirement files, to make it
suitable for testing. We might enable it to do this automatically. Basically it
pulls in the supported version of pipenv for a given Python.

.. code:: bash

    # For each python used:
    python -m pip install -r requirements.txt

    # Go to the base of this repository, may also go to sub-folders to
    # benefit from the structure.
    cd Nuitka-watch

    # Execute Nuitka watch. Nuitka does not have to be installed anywhere.
    python3 ../Nuitka/bin/nuitka-watch

    # Execute Nuitka watch in latest version (Py2C) against e.g. a hotfix in Nuitka-develop
    # with only 3.10 being done.
    python3 ./Py2C/bin/nuitka-watch --python-version=3.10 --nuitka-binary=../Nuitka-develop/bin/nuitka
