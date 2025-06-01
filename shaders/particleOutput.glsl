#version 430 core

uniform uint u_Width;
uniform uint u_Height;

uniform uint u_ParticleGridWidth;
uniform uint u_ParticleWidth;
uniform uint u_ParticleHeight;

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

    // calculate grid position
    ivec2 gridPos = ivec2(
        pos.x / u_ParticleWidth,
        (u_Height - pos.y - 1) / u_ParticleHeight);

    // else pick color
    // the order is BGRA
    uvec4 color;
    switch(particleGrid[gridPos.y * u_ParticleGridWidth + gridPos.x]) {
        case 0:  // empty
            color = uvec4(0);
            break;
        case 1:  // sand particle
            color = uvec4(0, 255, 255, 0);
            break;
    }

    // store color
    imageStore(outputImage, pos, color);
}
