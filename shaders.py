from OpenGL.GL import *

try:
    import OpenGL

    try:
        from OpenGL.GL import *  # this fails in <=2020 versions of Python on OS X 11.x
    except ImportError:
        print('Drat, patching for Big Sur')
        from ctypes import util

        orig_util_find_library = util.find_library


        def new_util_find_library(name):
            res = orig_util_find_library(name)
            if res: return res
            return '/System/Library/Frameworks/' + name + '.framework/' + name


        util.find_library = new_util_find_library
except ImportError:
    pass


def load_shaders(vertex_shader_source, fragment_shader_source):
    vertex_shader_id = glCreateShader(GL_VERTEX_SHADER)
    fragment_shader_id = glCreateShader(GL_FRAGMENT_SHADER)

    glShaderSource(vertex_shader_id, vertex_shader_source)
    glShaderSource(fragment_shader_id, fragment_shader_source)

    glCompileShader(vertex_shader_id)
    if not glGetShaderiv(vertex_shader_id, GL_COMPILE_STATUS):
        print(glGetShaderInfoLog(vertex_shader_id).decode())
        raise RuntimeError("Erro de compilacao do Vertex Shader")

    glCompileShader(fragment_shader_id)
    if not glGetShaderiv(fragment_shader_id, GL_COMPILE_STATUS):
        print(glGetShaderInfoLog(fragment_shader_id).decode())
        raise RuntimeError("Erro de compilacao do Vertex Shader")

    program_id = glCreateProgram()

    glAttachShader(program_id, vertex_shader_id)
    glAttachShader(program_id, fragment_shader_id)

    glLinkProgram(program_id)

    if not glGetProgramiv(program_id, GL_LINK_STATUS):
        print(glGetProgramInfoLog(program_id))
        raise RuntimeError('Linking error')

    return program_id
