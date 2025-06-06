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
        self.particle_grid: mgl.Buffer = self.ctx.buffer(reserve=self.board.nbytes)
        self.processed_grid: mgl.Buffer = self.ctx.buffer(reserve=self.particle_grid.size)

        # bind storage buffers
        self.particle_grid.bind_to_storage_buffer(1)
        self.processed_grid.bind_to_storage_buffer(2)

        # load shader
        with open("shaders/particleCompute.glsl", "r", encoding="utf-8") as file:
            self._compute: mgl.ComputeShader = self.ctx.compute_shader(file.read())

    def simulation_step(self):
        """
        Makes a step in simulation
        """

        # write data to buffers
        self.particle_grid.write(self.board.tobytes())

        # clear processed buffer
        self.processed_grid.clear()

        # put uniforms
        self._compute["u_Width"] = self.width
        self._compute["u_Height"] = self.height

        # calculate work group
        work_group_size = (16, 16, 1)
        num_groups_x = (self.width + work_group_size[0] - 1) // work_group_size[0]
        num_groups_y = (self.height + work_group_size[1] - 1) // work_group_size[1]
        num_groups_z = work_group_size[2]

        # dispatch the shader
        self._compute.run(group_x=num_groups_x, group_y=num_groups_y, group_z=num_groups_z)

        # write buffer data to board
        self.board = np.copy(np.frombuffer(self.processed_grid.read(), dtype=self.board.dtype))
