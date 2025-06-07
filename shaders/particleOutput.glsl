#version 430 core

uniform uint u_Width;
uniform uint u_Height;

uniform uint u_ParticleWidth;
uniform uint u_ParticleHeight;

// output image
layout(rgba8ui, binding = 0) uniform writeonly uimage2D outputImage;

// particle board
layout(r8ui, binding = 1) uniform readonly uimage2D particleGrid;

// color palette
layout(std430, binding = 3) buffer ColorPalette {
    uvec4 colorPalette[];
};

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

    uvec4 color = colorPalette[imageLoad(particleGrid, gridPos).r];

    // store color
    imageStore(outputImage, pos, color);
}
