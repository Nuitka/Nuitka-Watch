# nuitka-project: --mode=standalone

from sqlglot import transpile

print(transpile("SELECT * FROM foo", write="spark", pretty=True, identity=True)) # prints ['SELECT\n  *\nFROM foo']
print("OK")