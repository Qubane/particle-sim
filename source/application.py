"""
Application class
"""


import random
import moderngl as gl
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

    def run(self):
        """
        Runs the application
        """
