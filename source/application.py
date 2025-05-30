"""
Application class
"""


import os
import math
import time
import pygame
from source.gpu_process import *
from source.cpu_process import SingleCPUSimulation


class App:
    """
    Application class
    """

    def __init__(self):
        # pygame things
        pygame.init()

        # pygame window
        self.window_width: int = 800
        self.window_height: int = 600
        self.window = pygame.display.set_mode((self.window_width, self.window_height))

        # pygame window caption
        pygame.display.set_caption("Particles")

        # application loop
        self.running = False

        # board_mode of execution
        # 0 - Single core CPU
        # 1 - Compute GPU
        self.board_mode: int = 0

        # grid_width and grid_height
        self.grid_width: int = 120
        self.grid_height: int = 30

        # pick board
        if self.board_mode == 0:
            self.board: SingleCPUSimulation = SingleCPUSimulation(self.grid_width, self.grid_height)

        elif self.board_mode == 1:
            ...

        else:
            raise NotImplementedError

    def run(self):
        """
        Runs the application
        """

        # set running to True
        self.running = True

        # application loop
        while self.running:
            # render image
            self.process_render()

            # process events
            self.process_events()

            # process logic
            self.process_logic()

    def process_events(self):
        """
        Processes window events
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def process_render(self):
        """
        Processes window rendering
        """

        # update image
        pygame.display.flip()

    def process_logic(self):
        """
        Process "game" logic
        """

        # sinusoidal movement for brush
        x = (math.sin(time.perf_counter() / 2) + 1) / 2 * self.grid_width
        self.board.brush(x, self.grid_height * 0.8, 1, 3.5)

        # make a simulation step
        self.board.simulation_step()
