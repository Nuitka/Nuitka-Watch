# nuitka-project: --standalone
# nuitka-project: --noinclude-default-mode=error
# nuitka-project: --noinclude-custom-mode=numpy.distutils:error
# nuitka-project: --noinclude-numba-mode=allow 

import os

import pandas
import pandas._libs.tslibs.base
import pandas._libs.window
from pandas.io.formats.style import Styler

df = pandas.DataFrame({"a": [1, 2], "b": [3, 4]})
df.to_feather("test-data.feather")
print(pandas.read_feather("test-data.feather"))
os.unlink("test-data.feather")
print("OK")
