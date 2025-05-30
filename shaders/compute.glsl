#version 430 core

layout(std430, binding = 0) buffer ParticleGrid {
    int particleGrid[];
};

layout(std430, binding = 1) buffer ProcessedGrid {
    int processedGrid[];
};

layout(local_size_x = 16, local_size_y = 16) in;
void main() {
    ivec2 coord = ivec2(gl_GlobalInvocationID.xy);
}
