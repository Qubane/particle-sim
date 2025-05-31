#version 430 core

uniform uint u_Width;
uniform uint u_Height;

layout(std430, binding = 0) buffer ParticleGrid {
    uint particleGrid[];
};

layout(std430, binding = 1) buffer ProcessedGrid {
    uint processedGrid[];
};

layout(local_size_x = 16, local_size_y = 16) in;
void main() {
    // global id
    uvec2 globalId = gl_GlobalInvocationID.xy;

    // if it exceeds bounds
    if (globalId.x >= u_Width || globalId.y >= u_Height)
        return;

    // calculate index
    uint index = globalId.y * u_Width + globalId.x;

    // do nothing basically
    processedGrid[index] = particleGrid[index];
}
