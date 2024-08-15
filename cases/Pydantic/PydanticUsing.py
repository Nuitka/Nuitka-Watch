# nuitka-project: --standalone

from __future__ import print_function

from pydantic import BaseModel


class Test(BaseModel):
    title: str
    value: int


test = Test(title="Title", value=0)
print("Pydantic model", test)

print("OK")
