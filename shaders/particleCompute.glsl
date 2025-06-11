#version 430 core

uniform uint u_Width;
uniform uint u_Height;

// imput / unprocessed grid
layout(r8ui, binding = 1) uniform readonly uimage2D particleGrid;

// output grid
layout(r8ui, binding = 2) uniform writeonly uimage2D processedGrid;

uint get_unbound(int x, int y) {
    return imageLoad(particleGrid, ivec2(x, y)).r;
}

uint get_bound(int x, int y) {
    if (x > -1 && x < u_Width && y > -1 && y < u_Height)
        return imageLoad(particleGrid, ivec2(x, y)).r;
    return 1u;
}

void put_unbound(int x, int y, uint val) {
    imageStore(processedGrid, ivec2(x, y), uvec4(val));
}

layout(local_size_x = 16, local_size_y = 16) in;
void main() {
    // global id
    ivec2 pos = ivec2(gl_GlobalInvocationID.xy);

    // if it exceeds bounds
    if (pos.x >= u_Width || pos.y >= u_Height)
        return;

    // get current particle
    uint particle = get_unbound(pos.x, pos.y);

    // if it's empty -> return
    if (particle == 0) {
        return;
    }

    // any particle
    // if particle can go down -> do & exit
    if (get_bound(pos.x, pos.y - 1) == 0) {
        put_unbound(pos.x, pos.y, 0);
        put_unbound(pos.x, pos.y - 1, particle);
    }

    // check particles to the left
    else if (get_bound(pos.x - 1, pos.y) == 0 &&
        get_bound(pos.x - 2, pos.y) == 0 &&
        get_bound(pos.x - 1, pos.y - 1) == 0) {

        put_unbound(pos.x, pos.y, 0);
        put_unbound(pos.x - 1, pos.y - 1, particle);
    }

    // check particles to the right
    else if (get_bound(pos.x + 1, pos.y) == 0 &&
             get_bound(pos.x + 2, pos.y) == 0 &&
             get_bound(pos.x + 1, pos.y - 1) == 0) {

        put_unbound(pos.x, pos.y, 0);
        put_unbound(pos.x + 1, pos.y - 1, particle);
    }

    // place particle
    else {
        put_unbound(pos.x, pos.y, particle);
    }
}
