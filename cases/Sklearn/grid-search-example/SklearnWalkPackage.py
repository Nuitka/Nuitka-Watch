# nuitka-project: --standalone
# nuitka-project: --noinclude-default-mode=error
# nuitka-project: --include-package=sklearn
# nuitka-project: --nofollow-import-to=sklearn.*.tests
# nuitka-project: --nofollow-import-to=sklearn.tests
# nuitka-project: --nofollow-import-to=sklearn.conftest
# nuitka-project: --nofollow-import-to=sklearn._build_utils
# nuitka-project: --noinclude-custom-mode=matplotlib:warning
# nuitka-project: --noinclude-custom-mode=pandas:warning

## nuitka-project: --nofollow-import-to=sklearn.utils._testing
## nuitka-project: --noinclude-custom-mode=sklearn.utils._testing:error


from __future__ import print_function

import importlib
import pkgutil
import sys

# For coverage right now.
import sklearn


def walkPackage(package_name, package):
    print("Walk", package)

    for item in pkgutil.iter_modules(package.__path__):
        if item.name == "tests":
            continue

        full_name = "%s.%s" % (package_name, item.name)
        print("Containing", item, full_name)

        importlib.import_module(full_name)
        imported = sys.modules[full_name]
        print(imported)

        if item.ispkg:
            walkPackage(full_name, imported)


walkPackage("sklearn", sklearn)
