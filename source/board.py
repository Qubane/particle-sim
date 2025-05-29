"""
Particle board class
"""


import numpy as np


class Board:
    """
    2D grid of particles
    """

    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height

        self.board: np.ndarray = np.zeros((self.width, self.height), dtype=np.uint8)

    def plot(self, x_pos: int, y_pos: int, value: int):
        """
        Plots a particle at a given coordinate
        :param x_pos: x position
        :param y_pos: y position
        :param value: particle value (id)
        """

    def get(self, x_pos: int, y_pos: int) -> int:
        """
        Gets a particle from a given coordinate
        :param x_pos: x position
        :param y_pos: y position
        :return: particle value (id)
        """

    def brush(self, x_pos: int, y_pos: int, value: int, size: float = 1.0):
        """
        Draws with a circular brush at a given coordinate
        :param x_pos: x position
        :param y_pos: y position
        :param value: particle value (id)
        :param size: brush size
        """
