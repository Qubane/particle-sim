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
