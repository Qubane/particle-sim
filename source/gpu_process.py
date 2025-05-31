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
        self.ctx = mgl.create_context(standalone=True)

        # load shader
        with open("shaders/compute.glsl", "r", encoding="utf-8") as file:
            self._compute: mgl.ComputeShader = self.ctx.compute_shader(file.read())

    def simulation_step(self):
        """
        Makes a step in simulation
        """

        # create buffers
        particle_grid = self.ctx.buffer(data=self.board.tobytes())
        processed_grid = self.ctx.buffer(reserve=particle_grid.size)

        # bind storage buffers
        particle_grid.bind_to_storage_buffer(0)
        processed_grid.bind_to_storage_buffer(1)

        # calculate work group
        work_group_size = (16, 16, 1)
        num_groups_x = (self.width + work_group_size[0] - 1) // work_group_size[0]
        num_groups_y = (self.height + work_group_size[1] - 1) // work_group_size[1]
        num_groups_z = work_group_size[2]

        # dispatch the shader
        self._compute.run(group_x=num_groups_x, group_y=num_groups_y, group_z=num_groups_z)

        # write buffer data to board
        self.board = np.frombuffer(bytearray(processed_grid.read()), dtype=self.board.dtype)
