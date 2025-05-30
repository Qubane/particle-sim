"""
Use CPU to process the board
"""


import random
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

        # make copy of grid
        new = np.copy(self.board)

        # go through all particles, and process them
        for y in range(self.height):
            for x in range(self.width):
                # if self is empty -> skip
                if self.board[y * self.width + x] < 1:
                    continue

                # any particle
                # if particle can go down -> go
                if self.get(x, y - 1) == 0:
                    new[(y - 1) * self.width + x] = new[y * self.width + x]
                    new[y * self.width + x] = 0
                    continue

                # fetch 4 particles (2 on left, 2 on right)
                left = (
                    self.get(x - 1, y) == 0,
                    self.get(x - 2, y) == 0)
                right = (
                    self.get(x + 1, y) == 0,
                    self.get(x + 2, y) == 0
                )

                # if all are empty
                if all(left) and all(right):
                    # check spaces below
                    spaces = (
                        self.get(x - 1, y - 1) == 0,
                        self.get(x + 1, y - 1) == 0)

                    # if both space
                    if all(spaces):
                        # pick random space
                        if random.randint(0, 1):
                            new[(y - 1) * self.width + (x - 1)] = new[y * self.width + x]
                            new[y * self.width + x] = 0
                        else:
                            new[(y - 1) * self.width + (x + 1)] = new[y * self.width + x]
                            new[y * self.width + x] = 0

                    # if left is empty -> go
                    elif spaces[0]:
                        new[(y - 1) * self.width + (x - 1)] = new[y * self.width + x]
                        new[y * self.width + x] = 0

                    # if right is empty -> go
                    elif spaces[1]:
                        new[(y - 1) * self.width + (x + 1)] = new[y * self.width + x]
                        new[y * self.width + x] = 0

                # if only left is empty
                elif all(left):
                    if self.get(x - 1, y - 1) == 0:
                        new[(y - 1) * self.width + (x - 1)] = new[y * self.width + x]
                        new[y * self.width + x] = 0

                # if only right is empty
                elif all(right):
                    if self.get(x + 1, y - 1) == 0:
                        new[(y - 1) * self.width + (x + 1)] = new[y * self.width + x]
                        new[y * self.width + x] = 0

        # copy the new board
        self.board = new
