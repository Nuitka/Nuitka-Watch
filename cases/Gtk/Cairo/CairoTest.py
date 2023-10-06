# nuitka-project: --standalone
# nuitka-project: --include-data-file={MAIN_DIRECTORY}/Example-Icon.png=Example-Icon.png

import os

import cairo
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk, Gtk

Gtk.init()

image = cairo.ImageSurface.create_from_png(os.path.join(os.path.dirname(__file__), "Example-Icon.png"))
region = Gdk.cairo_region_create_from_surface(image)

print("All OK")
