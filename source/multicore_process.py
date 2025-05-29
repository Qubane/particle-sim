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

                # if void -> skip
                if particle < 1:
                    continue

                # neighbor particles (on left and right)
                left, right = self.get(x - 1, y), self.get(x + 1, y)

                # all particles
                # if particle can go down -> do so
                if self.get(x, y - 1) == 0:
                    # copy particle down
                    new[(y - 1) * self.width + x] = new[y * self.width + x]

                    # delete from current position
                    new[y * self.width + x] = 0

                # both neighbors are empty
                elif left == 0 and right == 0:
                    # neighbors below
                    b_left, b_right = self.get(x - 1, y - 1), self.get(x + 1, y - 1)

                    # if both neighbors are clear
                    if b_left == 0 and b_right == 0:
                        # coin flip
                        coin = random.randint(0, 1)

                        if coin == 0:
                            new[(y - 1) * self.width + (x - 1)] = new[y * self.width + x]
                            new[y * self.width + x] = 0
                        else:
                            new[(y - 1) * self.width + (x + 1)] = new[y * self.width + x]
                            new[y * self.width + x] = 0
                    elif b_left == 0:
                        new[(y - 1) * self.width + (x - 1)] = new[y * self.width + x]
                        new[y * self.width + x] = 0
                    elif b_right == 0:
                        new[(y - 1) * self.width + (x + 1)] = new[y * self.width + x]
                        new[y * self.width + x] = 0
                    else:
                        pass

                # only left neighbor is free
                elif left == 0:
                    if self.get(x - 1, y - 1) == 0:
                        new[(y - 1) * self.width + (x - 1)] = new[y * self.width + x]
                        new[y * self.width + x] = 0

                # only right neighbor is free
                elif right == 0:
                    if self.get(x + 1, y - 1) == 0:
                        new[(y - 1) * self.width + (x + 1)] = new[y * self.width + x]
                        new[y * self.width + x] = 0

                # no neighbors are free
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
