# nuitka-project: --mode=standalone

from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp

Window.size = (360, 640)

kv = """
MDRaisedButton:
    text: "Button"
    pos_hint: {"center_x":0.5,"center_y":0.5}
"""


class kivy(MDApp):
    def build(self):
        return Builder.load_string(kv)


kivy().run()
