"""
Application class
"""

import os
import math
import time
import pygame
from source.board import ParticleColor
from source.gpu_process import GPUSimulation
from source.cpu_process import SingleCPUSimulation


class App:
    """
    Application class
    """

    def __init__(self):
        # pygame things
        pygame.init()

        # pygame window
        self.window_width: int = 1280
        self.window_height: int = 720
        self.window = pygame.display.set_mode((self.window_width, self.window_height))

        # pygame window caption
        pygame.display.set_caption("Particles")

        # application loop
        self.running: bool = False
        self.framerate: int = 25

        # board_mode of execution
        # 0 - Single core CPU
        # 1 - Compute GPU
        self.board_mode: int = 0

        # grid_width and grid_height
        self.grid_width: int = 160
        self.grid_height: int = 90

        # pick board
        # CPU
        if self.board_mode == 0:
            self.board: SingleCPUSimulation = SingleCPUSimulation(self.grid_width, self.grid_height)

        # GPU
        elif self.board_mode == 1:
            self.board: GPUSimulation = GPUSimulation(self.grid_width, self.grid_height)

        # error
        else:
            raise NotImplementedError

    def run(self):
        """
        Runs the application
        """

        # set running to True
        self.running = True

        # application loop
        clk = pygame.time.Clock()
        while self.running:
            # render image
            self.process_render()

            # process events
            self.process_events()

            # process logic
            self.process_logic()

            # wait till next frame
            clk.tick(self.framerate)

    def process_events(self):
        """
        Processes window events
        """

        # go through events
        for event in pygame.event.get():
            # if window exit was pressed
            if event.type == pygame.QUIT:
                self.running = False

    def process_render(self):
        """
        Processes window rendering
        """

        # clear display
        self.window.fill(0)

        # calculate size of particles
        particle_size_x = math.ceil(self.window_width / self.grid_width)
        particle_size_y = math.ceil(self.window_height / self.grid_height)

        # render particle board to window
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                # if particle is empty -> skip
                if self.board.board[(self.grid_height - y - 1) * self.grid_width + x] < 1:
                    continue

                # calculate rectangle
                rect = (
                    x * particle_size_x, y * particle_size_y,  # position
                    particle_size_x,     particle_size_y       # size
                )

                # draw rectangle
                pygame.draw.rect(self.window, ParticleColor.SAND, rect)

        # update image
        pygame.display.flip()

    def process_logic(self):
        """
        Process "game" logic
        """

        # sinusoidal movement for brush
        x = (math.sin(time.perf_counter() / 2) + 1) / 2 * self.grid_width
        self.board.brush(x, self.grid_height * 0.8, 1, 3.0)

        # make a simulation step
        self.board.simulation_step()
