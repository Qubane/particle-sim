"""
Application class
"""

import math
import time
import pygame
import numpy as np
import moderngl as mgl
from source.board import ParticleColor, Board
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
        self.window_width: int = 1600
        self.window_height: int = 900
        self.window = pygame.display.set_mode((self.window_width, self.window_height))

        # pygame window caption
        pygame.display.set_caption("Particles")

        # moderngl
        self.ctx: mgl.Context = mgl.create_context(require=430, standalone=True)

        # moderngl shader
        with open("shaders/particleOutput.glsl", "r", encoding="utf-8") as file:
            self._particle_output: mgl.ComputeShader = self.ctx.compute_shader(file.read())

        # moderngl render
        self.texture: mgl.Texture = self.ctx.texture(
            size=(self.window_width, self.window_height),
            components=4,
            dtype="u1")

        # moderngl storage buffer
        self.particle_grid: mgl.Texture | None = None

        # application loop
        self.running: bool = False
        self.framerate: int = 60

        # grid_width and grid_height
        self.grid_width: int = self.window_width
        self.grid_height: int = self.window_height

        # board mode of execution
        self.process_mode: int = 1

        # particle board
        self.board: Board | None = None

        # update board mode
        self.update_board_mode()

    def update_board_mode(self):
        """
        Updates board mode
        """

        # check if particle board already exists
        particles = None
        if self.board is not None:
            # save the array of particles
            particles = self.board.board

        # pick board
        # CPU
        if self.process_mode == 0:
            self.board: SingleCPUSimulation = SingleCPUSimulation(self.grid_width, self.grid_height)

            # if particle grid does not exist
            if self.particle_grid is None:
                # create buffer
                self.particle_grid = self.ctx.texture(
                    size=(self.board.width, self.board.height),
                    components=1,
                    dtype="u1")

                # bind the storage buffer
                self.particle_grid.bind_to_image(1)

        # GPU
        elif self.process_mode == 1:
            self.board: GPUSimulation = GPUSimulation(self.grid_width, self.grid_height)
            # no need to create a buffer here, it could be reused instead

        # error
        else:
            raise NotImplementedError

        # put the particles back
        if particles is not None:
            self.board.board = particles

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
            # if window exit was pressed -> exit
            if event.type == pygame.QUIT:
                self.running = False

            # if keyboard was pressed
            elif event.type == pygame.KEYDOWN:
                # if ESC key was pressed -> exit
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                # if number 1 was pressed -> switch mode to 0
                elif event.key == pygame.K_1:
                    self.process_mode = 0
                    self.update_board_mode()

                # if number 2 was pressed -> switch mode to 1
                elif event.key == pygame.K_2:
                    self.process_mode = 1
                    self.update_board_mode()

    def process_render(self):
        """
        Processes window rendering
        """

        # bind image buffer
        self.texture.bind_to_image(0)

        # check if CPU render
        if self.process_mode == 0:
            # write data to buffer
            self.particle_grid.write(self.board.board.tobytes())

        # put uniforms
        self._particle_output["u_Width"] = self.window_width
        self._particle_output["u_Height"] = self.window_height
        self._particle_output["u_ParticleWidth"] = math.ceil(self.window_width / self.grid_width)
        self._particle_output["u_ParticleHeight"] = math.ceil(self.window_height / self.grid_height)

        # calculate work group
        work_group_size = (16, 16, 1)
        num_groups_x = (self.window_width + work_group_size[0] - 1) // work_group_size[0]
        num_groups_y = (self.window_height + work_group_size[1] - 1) // work_group_size[1]
        num_groups_z = work_group_size[2]

        # dispatch the shader
        self._particle_output.run(group_x=num_groups_x, group_y=num_groups_y, group_z=num_groups_z)

        # blit the texture
        self.texture.read_into(self.window.get_buffer())

        # update image
        pygame.display.flip()

    def process_logic(self):
        """
        Process "game" logic
        """

        # sinusoidal movement for brush
        x = (math.sin(time.perf_counter() / 2) + 1) / 2 * self.grid_width
        self.board.brush(x, self.grid_height * 0.8, 1, 5.0)

        # make a simulation step
        self.board.simulation_step()
