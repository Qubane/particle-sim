"""
Application class
"""


import moderngl as gl


class App:
    """
    Application class
    """

    def __init__(self):
        self.ctx: gl.Context = gl.create_context()

        with open("shaders/compute.glsl", "r", encoding="ascii") as file:
            self.compute_shader: gl.ComputeShader = self.ctx.compute_shader(file.read())

    def run(self):
        """
        Runs the application
        """
