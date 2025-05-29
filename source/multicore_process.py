"""
Use CPU to process the board
"""


import numpy as np
from source.board import Board


class SingleCPUSimulation(Board):
    """
    Single core CPU processed particle simulation
    """

    def simulation_step(self):
        """
        Makes a step in simulation
        """


class MultipleCPUSimulation(Board):
    """
    Multicore CPU processed particle simulation
    """

    def simulation_step(self):
        """
        Makes a step in simulation
        """
