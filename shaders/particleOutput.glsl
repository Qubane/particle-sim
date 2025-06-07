#version 430 core

uniform uint u_Width;
uniform uint u_Height;

uniform uint u_ParticleWidth;
uniform uint u_ParticleHeight;

// output image
layout(rgba8ui, binding = 0) uniform writeonly uimage2D outputImage;

// particle board
layout(r8ui, binding = 1) uniform readonly uimage2D particleGrid;

layout(local_size_x = 16, local_size_y = 16) in;
void main() {
    // get position
    ivec2 pos = ivec2(gl_GlobalInvocationID.xy);

    // skip if position is out of bounds
    if (pos.x >= u_Width || pos.y >= u_Height)
        return;

    // calculate grid position
    ivec2 gridPos = ivec2(
        pos.x / u_ParticleWidth,
        (u_Height - pos.y - 1) / u_ParticleHeight);

    // else pick color
    // the order is BGRA
    uvec4 color;
    switch(imageLoad(particleGrid, gridPos).r) {
        case 0:  // empty
            color = uvec4(0);
            break;
        case 1:  // sand particle
            color = uvec4(0, 255, 255, 0);
            break;
        case 2:  // water particle
            color = uvec4(255, 32, 0, 0);
            break;
    }

    // store color
    imageStore(outputImage, pos, color);
}
