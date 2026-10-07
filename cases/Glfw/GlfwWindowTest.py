# nuitka-project: --mode=standalone

# spell-checker: ignore glfw

import glfw


def main():
    if not glfw.init():
        raise RuntimeError("Failed to initialize GLFW")

    try:
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

        # Avoid requiring an OpenGL context for the smoke test, if supported.
        try:
            glfw.window_hint(glfw.CLIENT_API, glfw.NO_API)
        except AttributeError:
            pass

        window = glfw.create_window(64, 64, "Nuitka GLFW window test", None, None)

        if not window:
            raise RuntimeError("Failed to create GLFW window")

        try:
            print("Window size:", "%sx%s" % glfw.get_window_size(window))
        finally:
            glfw.destroy_window(window)
    finally:
        glfw.terminate()

    print("GLFW version:", glfw.get_version())
    print("OK")


if __name__ == "__main__":
    main()
