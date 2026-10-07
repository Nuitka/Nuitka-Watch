# nuitka-project: --mode=standalone

# spell-checker: ignore glfw

import os

import glfw


def main():
    if not glfw.init():
        raise RuntimeError("Failed to initialize GLFW")

    try:
        # Avoid requiring an OpenGL context for this window, if supported.
        try:
            glfw.window_hint(glfw.CLIENT_API, glfw.NO_API)
        except AttributeError:
            pass

        window = glfw.create_window(
            400, 300, "Nuitka GLFW interactive test", None, None
        )

        if not window:
            raise RuntimeError("Failed to create GLFW window")

        glfw.show_window(window)
        glfw.set_window_title(window, "Nuitka GLFW interactive test, press ESC")

        # Allow automated smoke execution of this interactive program.
        if os.getenv("NUITKA_TEST_INTERACTIVE") == "0":
            glfw.poll_events()
            glfw.set_window_should_close(window, True)

        while not glfw.window_should_close(window):
            glfw.poll_events()

            if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
                glfw.set_window_should_close(window, True)

        glfw.destroy_window(window)
    finally:
        glfw.terminate()

    print("GLFW version:", glfw.get_version())
    print("OK")


if __name__ == "__main__":
    main()
