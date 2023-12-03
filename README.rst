Nuitka Watch
============

This repository is under construction. The intention is twofold, to detect
PyPI package updates, and check if Nuitka is working with them, and for
Nuitka updates, if it still handles everything in a good way.

One main goal is to detect ``scipy`` breaking on a platform with Nuitka due
to DLL changes right away, and not have to wait until somebody reports it, 
and then probably not in the correct fashion. Packages covered here have a
chance to generate automatic reports when they break.

The other idea is to detect regressions inside the Nuitka plugin mechanisms
and standalone capabilities automatically. DLLs not included anymore, anti-bloat
changes that do not apply anymore, and of course code enhancements in Nuitka that
fail to neglect all cases into account and break existing stuff.

And another important idea, is to do all of that in a distributed and automated
fashion, because there is no way for one user to compile everything on all 
platforms for every release of Nuitka and for every PyPI package. We don't
have that yet, but you should be able to set up your own form of watching
the packages you care about.

The ``nuitka-watch`` tool will scan for installed Pythons. Right now you are
expected to install the dependencies in the requirement file, to make it
suitable for testing. We might enable it to do this automatically. Basically, it
pulls in the supported version of ``pipenv`` for a given Python.

.. code:: bash

    # Go to the base of this repository, may also go to sub-folders to
    # benefit from the structure.
    cd Nuitka-watch

    # For each python used:
    python -m pip install -r requirements.txt

    # Execute Nuitka watch in latest version (Py2C) against e.g. a hotfix in Nuitka-develop
    # with only 3.10 being done, but no PyPI updates.
    # python3 ../Py2C/bin/nuitka-watch --python-version=3.10 --no-pipenv-update --nuitka-binary=../Nuitka-develop/bin/nuitka
    ./nuitka-release.sh

    # Execute Nuitka watch in latest version (Py2C) against e.g. a hotfix in Nuitka-develop
    # with only 3.10 being done, and also PyPI updates, which may break Nuitka potentially.
    # python3 ../Py2C/bin/nuitka-watch --python-version=3.10 --nuitka-binary=../Nuitka-develop/bin/nuitka
    ./pypi-update.sh
