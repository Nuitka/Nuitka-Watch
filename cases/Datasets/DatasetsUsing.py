# nuitka-project: --mode=standalone

from datasets import Dataset
print(Dataset.from_list([{"a":1}]))
print("OK.")