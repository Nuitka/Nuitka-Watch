import os

from delphifmx import *


class Form3(Form):
    def __init__(self, owner):
        self.Button1 = None
        self.GroupBox1 = None
        self.CheckBox1 = None
        self.PopupBox1 = None
        self.Label1 = None
        self.Button2 = None
        self.LoadProps(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "Unit3.pyfmx")
        )

    def Button1Click(self, Sender):
        pass

    def Button2Click(self, Sender):
        pass
