# nuitka-project: --standalone

# Requires GTK packages on the system:
# apt-get install --no-install-recommends libgirepository1.0-dev libcairo

import toga
import sys

def button_handler(widget):
    print("hello")

def build(app):
    box = toga.Box()
    button = toga.Button("Hello world", on_press=button_handler)
    button.style.padding = 50
    button.style.flex = 1
    box.add(button)
    return box

def main():
    return toga.App("First App", "org.nuitka.helloworld", startup=build)

if __name__ == "__main__":
    main()