"""
Particle board class
"""


import math
import numpy as np


class ParticleColor:
    """
    Colors for particles
    """

    EMPTY = (0, 0, 0, 0)
    SAND = (255, 255, 0, 255)
    DIRT = (139, 69, 19, 255)
    WATER = (0, 32, 255, 255)

    ALL: list[tuple[int]] = [
        EMPTY,
        SAND,
        DIRT,
        WATER
    ]

    GPU_BUF: np.ndarray = np.array(ALL, dtype=np.uint32)
    for i in range(len(GPU_BUF)):
        # RGBA -> BGRA
        GPU_BUF[i][0], GPU_BUF[i][2] = GPU_BUF[i][2], GPU_BUF[i][0]


class Board:
    """
    2D grid of particles
    """

    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height

        self.board: np.ndarray = np.zeros(self.width * self.height, dtype=np.uint8)

    def plot(self, x_pos: int | float, y_pos: int | float, value: int):
        """
        Plots a particle at a given coordinate
        :param x_pos: x position
        :param y_pos: y position
        :param value: particle value (id)
        """

        x_pos, y_pos = int(x_pos), int(y_pos)
        if 0 < x_pos < self.width and 0 < y_pos < self.height:
            self.board[y_pos * self.width + x_pos] = value

    def get(self, x_pos: int | float, y_pos: int | float) -> int:
        """
        Gets a particle from a given coordinate
        :param x_pos: x position
        :param y_pos: y position
        :return: particle value (id)
        """

        x_pos, y_pos = int(x_pos), int(y_pos)
        if 0 < x_pos < self.width and 0 < y_pos < self.height:
            return self.board[y_pos * self.width + x_pos]
        return -1

    def brush(self, x_pos: int | float, y_pos: int | float, value: int, size: float = 1.0):
        """
        Draws with a circular brush at a given coordinate
        :param x_pos: x position
        :param y_pos: y position
        :param value: particle value (id)
        :param size: brush size
        """

        for y in range(-math.ceil(size / 2), math.ceil(size / 2)):
            for x in range(-math.ceil(size / 2), math.ceil(size / 2)):
                distance = math.sqrt(x ** 2 + y ** 2) * 2

                brush_x = x_pos + x
                brush_y = y_pos + y

                if 0 < brush_x < self.width and 0 < brush_y < self.height and distance <= size:
                    self.plot(brush_x, brush_y, value)

    def simulation_step(self):
        """
        Makes a step in simulation
        """

        raise NotImplementedError
