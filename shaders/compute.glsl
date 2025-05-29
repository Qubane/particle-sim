#version 430 core

layout (local_size_x=1) in;

layout (std430, binding=0) buffer InputBufferA {
    int dataA[];
};

layout (std430, binding=1) buffer InputBufferB {
    int dataB[];
};

layout (std430, binding=2) buffer OutputBuffer {
    int result[];
};

void main() {
    uint index = gl_GlobalInvocationID.x;

    result[index] = dataA[index] * dataB[index];
}
