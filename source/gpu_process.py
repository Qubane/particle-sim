"""
Use GPU compute shaders to process the board
"""


import numpy as np
import moderngl as mgl
from source.board import Board


class GPUSimulation(Board):
    """
    GPU processed particle simulation
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create context
        self.ctx = mgl.get_context()

        # create buffers
        self.particle_grid: mgl.Texture = self.ctx.texture(
            size=(self.width, self.height),
            components=1,
            dtype="u1")
        self.processed_grid: mgl.Texture = self.ctx.texture(
            size=(self.width, self.height),
            components=1,
            dtype="u1")

        # bind storage buffers
        self.particle_grid.bind_to_image(1)
        self.processed_grid.bind_to_image(2)

        # load shader
        with open("shaders/particleCompute.glsl", "r", encoding="utf-8") as file:
            self._compute: mgl.ComputeShader = self.ctx.compute_shader(file.read())

    def simulation_step(self):
        """
        Makes a step in simulation
        """

        # write data to buffers
        self.particle_grid.write(self.board.tobytes())

        # put uniforms
        self._compute["u_Width"] = self.width
        self._compute["u_Height"] = self.height

        # calculate work group
        work_group_size = (16, 16)
        num_groups_x = (self.width + work_group_size[0] - 1) // work_group_size[0]
        num_groups_y = (self.height + work_group_size[1] - 1) // work_group_size[1]

        # dispatch the shader
        self._compute.run(group_x=num_groups_x, group_y=num_groups_y)

        # write buffer data to board
        self.board = np.copy(np.frombuffer(self.processed_grid.read(), dtype=self.board.dtype))
