"""
Application class
"""


import os
import math
import time
import random
import moderngl as gl
from source.board import Board
from source.gpu_process import *
from source.cpu_process import SingleCPUSimulation


class App:
    """
    Application class
    """

    def __init__(self):
        # mode of execution
        # 0 - Single core CPU
        # 1 - Compute GPU
        self.mode: int = 0

        # width and height
        self.width: int = 120
        self.height: int = 30

        # pick board
        if self.mode == 0:
            self.board: SingleCPUSimulation = SingleCPUSimulation(self.width, self.height)

        elif self.mode == 1:
            ...

        else:
            raise NotImplementedError

    def run(self):
        """
        Runs the application
        """

        os.system("cls" if os.name == "nt" else "clear")

        # self.board.brush(self.width // 2, self.height // 2, 1, 6.0)

        while True:
            # lil sinusoidal movement for brush
            x = (math.sin(time.perf_counter() / 2) + 1) / 2 * self.width
            self.board.brush(int(x), self.height // 2, 1, 3.0)

            # printout the board
            self._print_board()

            # make a simulation step
            self.board.simulation_step()

            # sleep to make 25'ish frames per second
            time.sleep(1 / 25)

    def _print_board(self):
        """
        Temporary. Prints the board to terminal
        """

        out = "\x1b[H"
        particles = self.width * self.height
        count = 0
        for i in range(particles - self.width):
            if i > 0 and i % self.width == 0:
                out += "\n"
            if self.board.board[particles - i - 1] > 0:
                count += 1
                out += "█"
            else:
                out += " "
        print(out, end="\n")
        print(f"p: {count}", end="", flush=True)
