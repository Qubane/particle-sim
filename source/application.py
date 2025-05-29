"""
Application class
"""


import random
import moderngl as gl


class App:
    """
    Application class
    """

    def __init__(self):
        self.ctx: gl.Context = gl.create_context(standalone=True)

        with open("shaders/compute.glsl", "r", encoding="ascii") as file:
            self.compute_shader: gl.ComputeShader = self.ctx.compute_shader(file.read())

    def run(self):
        """
        Runs the application
        """

        # size
        size = 32

        # create inputs
        input_data_a = random.randbytes(size)
        input_data_b = random.randbytes(size)

        # create buffers
        input_buffer_a = self.ctx.buffer(data=input_data_a)
        input_buffer_b = self.ctx.buffer(data=input_data_b)
        output_buffer = self.ctx.buffer(reserve=len(input_data_a))

        # bind buffers
        input_buffer_a.bind_to_storage_buffer(0)
        input_buffer_b.bind_to_storage_buffer(1)
        output_buffer.bind_to_storage_buffer(2)

        # dispatch compute shader
        local_group_size_x = 1
        group_size_x = (len(input_data_a) + local_group_size_x - 1) // local_group_size_x
        self.compute_shader.run(group_x=group_size_x)

        # readout data
        output_data = list(output_buffer.read())

        print(f"input A: {list(input_data_a)}")
        print(f"input B: {list(input_data_b)}")
        print(f"A * B: {output_data}")
