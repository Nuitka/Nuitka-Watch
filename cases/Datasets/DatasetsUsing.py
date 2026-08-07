# nuitka-project: --mode=standalone
# nuitka-project: --enable-plugin=dill-compat

from datasets import Dataset
print(Dataset.from_list([{"a":1}]))
print("OK.")