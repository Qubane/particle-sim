"""
Use GPU compute shaders to process the board
"""


import numpy as np
from source.board import Board


class GPUSimulation(Board):
    """
    GPU processed particle simulation
    """

    def simulation_step(self):
        """
        Makes a step in simulation
        """
