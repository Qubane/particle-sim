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
                # get particle (no boundary checks)
                particle = self.board[y * self.width + x]

                # if void / empty -> skip
                if particle < 1:
                    continue

                # any particle
                # if particle can go down -> go
                if self.get(x, y - 1) == 0:
                    new[(y - 1) * self.width + x] = new[y * self.width + x]
                    new[y * self.width + x] = 0
                    continue

                # check left and right
                left, right = self.get(x - 1, y), self.get(x + 1, y)
                left2, right2 = self.get(x - 2, y), self.get(x + 2, y)

                # if left and right are empty
                if left == 0 and left2 == 0 and right == 0 and right2 == 2:
                    # check left and right below
                    b_left, b_right = self.get(x - 1, y - 1), self.get(x + 1, y - 1)

                    # if both are empty -> go
                    if b_left == 0 and b_right == 0:
                        # move randomly down and left or right
                        if random.randint(0, 1):
                            new[(y - 1) * self.width + (x - 1)] = new[y * self.width + x]
                            new[y * self.width + x] = 0
                        else:
                            new[(y - 1) * self.width + (x + 1)] = new[y * self.width + x]
                            new[y * self.width + x] = 0

                    # if left is empty -> go
                    elif b_left == 0:
                        new[(y - 1) * self.width + (x - 1)] = new[y * self.width + x]
                        new[y * self.width + x] = 0

                    # if right is empty -> go
                    elif b_right == 0:
                        new[(y - 1) * self.width + (x + 1)] = new[y * self.width + x]
                        new[y * self.width + x] = 0

                    # else -> stay
                    else:
                        pass

                # if only left is empty
                elif left == 0 and left2 == 0:
                    if self.get(x - 1, y - 1) == 0:
                        new[(y - 1) * self.width + (x - 1)] = new[y * self.width + x]
                        new[y * self.width + x] = 0

                # if only right is empty
                elif right == 0 and right2 == 0:
                    if self.get(x + 1, y - 1) == 0:
                        new[(y - 1) * self.width + (x + 1)] = new[y * self.width + x]
                        new[y * self.width + x] = 0

                # else -> stay
                else:
                    pass

        # copy the new board
        self.board = new


class MultipleCPUSimulation(Board):
    """
    Multicore CPU processed particle simulation
    """

    def simulation_step(self):
        """
        Makes a step in simulation
        """
