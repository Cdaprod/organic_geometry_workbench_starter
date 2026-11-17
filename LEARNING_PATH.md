# From basic Python to procedural Blender: a practical path

## What you already know from the Doesbot Voronoi generator

Your script constructs a 2D height field:

1. `np.meshgrid(xs, ys)` creates coordinate locations.
2. Random `seeds` define Voronoi cell centers.
3. The two nearest seeds determine each point's cell-boundary distance.
4. `base + relief * field * fade` becomes the outer roof elevation.
5. The solid is converted into an SDF, smoothed, and meshed with marching cubes.

So **your generator is math first, mesh second**. `bpy` is not necessary for the mathematical field.

## Reusable mental model

```text
requirements and datums (JSON / FreeCAD)
        ↓
geometry recipe (curves, distance fields, Voronoi, lattice)
        ↓
constraint masks (holes, component keep-outs, minimum thickness)
        ↓
solid mesh (marching cubes / CAD kernel)
        ↓
validation (geometry + load/print engineering)
        ↓
STL → Blender visualization or FreeCAD assembly
```

## First exercise: change one camera-arm strut

Open `examples/camera_arm.json`. Find the connection between `elbow_bottom` and `bridge`:

- Change `control` from `[57,0,-12]` to `[57,0,-18]` to bend the strut downward.
- Keep the same mounting-node locations; neither bolt center moves.
- Run `python -m organic.build examples/camera_arm.json` again and inspect the preview.

This is how parametric modeling works: **design intent** resides in JSON; the script is a generic geometry compiler.

## Second exercise: change a structural radius

Change `radius_a_mm` from `4.2` to `5.0` for one strut. The beam thickens, but the bolt holes stay the same size.

The shape may look stronger, but that cannot be proven without boundary conditions, a material model and FEA. Local thickness and fastener failure must also be evaluated.

## Third exercise: make a new organic component

Copy the camera arm JSON, change its `name`, replace the node coordinates and mount locations, then connect them using the `struts` list. Generate again without changing any Python.

Useful future design files include:
- `camera_arm.json`: lightweight open-cell arms
- `monitor_mount.json`: mounting plates and internal load-path ribs
- `enclosure_lid.json`: heightmap-based shell + voids and keep-out geometry
- `cable_clip.json`: parametric compliant beams, with printable strain limits

The current SDF engine specifically implements **tubular struts and Y-axis bosses**. An enclosure generator needs additional field primitives such as boxes, roof-height surfaces, and variable-thickness shells; a flexible cable clip also needs compliant-deflection analysis.

## How to write your own operation

Make a new function in `organic/fields.py` that accepts NumPy grids `x,y,z` and returns a *signed distance*: negative inside the solid, positive outside.

Example sphere centered at `(cx,cy,cz)`:

```python
import numpy as np

def sphere_sdf(x, y, z, center, radius):
    cx,cy,cz = center
    return np.sqrt((x-cx)**2+(y-cy)**2+(z-cz)**2)-radius
```

Combine a new solid with an existing solid by taking the **minimum** of their SDFs. Subtract a keep-out region by taking the **maximum** of the solid SDF and the *negative* cutter SDF. Convert the resulting field to a mesh with marching cubes.

## Where Blender belongs

`bpy` provides Blender-specific responsibilities: adding objects/collections, assigning materials, procedural modifiers, cameras, renders, files and exports. The `blender_import.py` in this package demonstrates this as a **separate backend**.

For many shapes, Blender's curves (`Curve.bevel_depth`) are enough. For branching organic shapes, SDFs are often easier because union and smooth blending are mathematical operations rather than complex mesh repairs.

## What real topology optimization adds

A lattice designed by hand is topology-*inspired*. Actual topology optimization needs:

- A **design domain**: where material is allowed.
- **Non-design regions**: bolt bosses, mating surfaces and keep-outs.
- **Loads**: forces and moments on the camera and arm.
- **Supports**: constraints at fixed mounting bolts.
- **Material**: Young's modulus, Poisson ratio, and strength values.
- **Solver**: finite element analysis with a topology optimizer (e.g. density-based SIMP).
- **Manufacturing constraints**: print direction, overhangs, min printable feature size, fatigue, fastener bearing and local stability.

Only after optimizing these fields do you convert them into clean, editable geometry and validate them under the actual intended loading.

## CAD parameters worth standardizing

Each design should track mm, a named coordinate frame, mounting centers, hole/boss dimensions, cable/connector keep-out volumes, minimum wall and beam dimensions, generate seed, revision, and acceptance tests. Your FreeCAD master sketch can export these into JSON rather than having project scripts hard-code them.
