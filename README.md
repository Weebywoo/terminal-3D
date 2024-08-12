# terminal-3D

- https://stackoverflow.com/questions/54143142/3d-intersection-between-segment-and-triangle
- https://joshortner.github.io/raytracing-part-one
- https://paulbourke.net/geometry/polygonise/

## ToDo

- Implement perspective camera
- Implement proper ray casting
- Speed up ray casting (BVH, etc.)
- Multiprocessing:
    - Tried, but didn't yield speedups
- Organise code into pipeline style (research what that actually means)
- Add mouse controls
- Improve controls

## Steps

1. Application
    1. Controls
    2. Collision detection
    3. BVH
2. Geometry
    1. Model & camera transformation
        1. Camera coordinate system
        2. Camera transformation
    2. Projection
    3. Lighting
    4. Clipping
        1. Near clipping plane
        2. Far clipping plane
3. Rasterization
4. Screen