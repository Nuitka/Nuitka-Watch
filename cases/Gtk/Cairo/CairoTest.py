# nuitka-project: --standalone

import cairo
import gi
from gi.repository import Gdk, Gtk

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
Gtk.init()

image = cairo.ImageSurface.create_from_png("doc/images/Nuitka-Logo-Symbol.png")
region = Gdk.cairo_region_create_from_surface(image)

print("All OK")
