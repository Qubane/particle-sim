"""
Application class
"""


import random
import moderngl as gl
from source.board import Board
from source.gpu_process import *
from source.cpu_process import SingleCPUSimulation, MultipleCPUSimulation


class App:
    """
    Application class
    """

    def __init__(self):
        # mode of execution
        # 0 - Single core CPU
        # 1 - Multicore CPU
        # 2 - Compute GPU
        self.mode: int = 0

        # width and height
        self.width: int = 120
        self.height: int = 60

        # pick board
        if self.mode == 0:
            self.board: SingleCPUSimulation = SingleCPUSimulation(self.width, self.height)

        elif self.mode == 1:
            self.board: MultipleCPUSimulation = MultipleCPUSimulation(self.width, self.height)

        elif self.mode == 2:
            ...

        else:
            raise NotImplementedError

    def run(self):
        """
        Runs the application
        """
