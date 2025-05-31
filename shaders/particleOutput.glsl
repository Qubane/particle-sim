#version 430 core

uniform uint u_Width;
uniform uint u_Height;

// output image
layout(rgba8ui, binding = 0) uniform writeonly uimage2D outputImage;

// particle board
layout(std430, binding = 1) buffer ParticleGrid {
    uint particleGrid[];
};

layout(local_size_x = 16, local_size_y = 16) in;
void main() {
    // get position
    ivec2 pos = ivec2(gl_GlobalInvocationID.xy);

    // skip if position is out of bounds
    if (pos.x >= u_Width || pos.y >= u_Height)
        return;

    // else pick color
    vec4 color;
    switch(particleGrid[pos.y * u_Width + pos.x]) {
        case 0:  // empty
            return;
        case 1:  // sand particle
            color = vec4(1.0, 1.0, 0.0, 1.0);
            break;
    }

    // store color
    imageStore(outputImage, pos, uvec4(color * 255));
}
