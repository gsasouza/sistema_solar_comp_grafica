import glfw


def create_glfw_window(width=700, height=700):
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    window = glfw.create_window(width, height, "Sistema Solar", None, None)
    glfw.make_context_current(window)
    glfw.swap_interval(0)
    return window
