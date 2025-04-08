# nuitka-project: --mode=standalone

# nuitka-project: --include-data-file={MAIN_DIRECTORY}/link_target=link_target
# nuitka-project: --include-data-file={MAIN_DIRECTORY}/link_source=link_source
# nuitka-project: --include-data-file={MAIN_DIRECTORY}/subdir/link_source2=subdir/link_source2

import os

with open(os.path.join(os.path.dirname(__file__), "link_source")) as data_file:
    print(data_file.read())

with open(
    os.path.join(os.path.dirname(__file__), "subdir", "link_source2")
) as data_file:
    print(data_file.read())

print("OK")
