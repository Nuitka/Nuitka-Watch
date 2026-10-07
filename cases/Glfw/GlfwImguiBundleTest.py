# nuitka-project: --mode=standalone

# spell-checker: ignore glfw,imgui

import os
import sys

# Import order matters: pyglfw is imported first, and must already be
# pointed at the GLFW library that imgui_bundle ships, or the C++ backend
# of imgui_bundle will use a different GLFW library instance.
import glfw

import imgui_bundle


def getVendoredLibraries():
    """Get the GLFW libraries that imgui_bundle ships, if any."""
    search_dirs = [os.path.dirname(os.path.abspath(imgui_bundle.__file__))]

    native_module = sys.modules.get("imgui_bundle._imgui_bundle")

    if native_module is not None and getattr(native_module, "__file__", None):
        native_dir = os.path.dirname(os.path.abspath(native_module.__file__))

        search_dirs.append(native_dir)

        # Shared library dependencies of extension modules may be placed in
        # the main program directory instead of next to the module.
        search_dirs.append(os.path.dirname(native_dir))

    result = set()

    for search_dir in search_dirs:
        for filename in os.listdir(search_dir):
            if filename.startswith(("libglfw", "glfw3")):
                result.add(os.path.realpath(os.path.join(search_dir, filename)))

    return result


def checkSharedLibrary():
    """Check that pyglfw uses the GLFW library shipped by imgui_bundle."""
    if "__compiled__" not in globals():
        print("Not a compiled run, skipping library check.")
        return

    vendored_libraries = getVendoredLibraries()

    if not vendored_libraries:
        print("No GLFW library shipped by imgui_bundle, skipping library check.")
        return

    loaded_library = os.path.realpath(glfw.library.glfw._name)

    if loaded_library not in vendored_libraries:
        raise RuntimeError(
            "glfw loaded '%s' instead of the imgui_bundle provided '%s'."
            % (loaded_library, ", ".join(sorted(vendored_libraries)))
        )

    print("Using imgui_bundle GLFW library:", os.path.basename(loaded_library))


def main():
    checkSharedLibrary()

    if not glfw.init():
        raise RuntimeError("Failed to initialize GLFW")

    try:
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

        # Avoid requiring an OpenGL context for the smoke test, if supported.
        try:
            glfw.window_hint(glfw.CLIENT_API, glfw.NO_API)
        except AttributeError:
            pass

        window = glfw.create_window(
            64, 64, "Nuitka imgui_bundle GLFW test", None, None
        )

        if not window:
            raise RuntimeError("Failed to create GLFW window")

        try:
            if os.getenv("NUITKA_TEST_INTERACTIVE") != "0":
                glfw.show_window(window)

                while not glfw.window_should_close(window):
                    glfw.poll_events()
        finally:
            glfw.destroy_window(window)
    finally:
        glfw.terminate()

    print("GLFW version:", glfw.get_version())
    print("OK")


if __name__ == "__main__":
    main()
