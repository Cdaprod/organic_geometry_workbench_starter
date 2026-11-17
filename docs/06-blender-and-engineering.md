# 06 — Where Blender belongs, and where topology optimization begins

We've built shapes without opening Blender. This separation is intentional: **NumPy computes the structure; Blender can present it**.

## A simple division of responsibilities

| Tool | Best role in this project |
|---|---|
| Python + NumPy | Coordinate math, curves, SDF expressions, design-file parsing |
| scikit-image | Marching-cubes isosurface extraction |
| trimesh | Mesh inspection, bounds, volume and STL export |
| `bpy` | Blender scene creation, materials, mesh visualization, rendering |
| FreeCAD | Sketch constraints, CAD datum references, dimension-critical interfaces |
| FEA / optimization tools | Stress, displacement, buckling, topology optimization under load cases |

`blender_import.py` imports an STL, adds a material and lighting, sets an orthographic camera and saves a `.blend` and PNG. Smoothing its shading normals improves its appearance; it does **not** improve the manufacturing geometry.

## Render the first arm

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background \
  --python blender_import.py -- results/first_arm/first_arm.stl
```

On other systems change only the Blender executable path. The `--` separates Blender arguments from the Python script's arguments.

Ask yourself: if you change a mesh's metallic material, do you change the strut's radius? No. If you change the source JSON and rebuild, do you change physical geometry? Yes. This is an important separation when automating CAD.

## Why the robot-arm inspiration is not the same as optimization

A photo of a branched, organic bracket might have been created by artist modeling, Voronoi/lattice design, or actual topology optimization. Appearance alone cannot tell you which.

A real topology-optimization process needs:

1. **Design domain**: where material is allowed.
2. **Non-design areas**: bolts, bearing pads, mating interfaces, keep-outs.
3. **Loads and supports**: forces, moments, constraints, and use cases.
4. **Material properties**: modulus, Poisson ratio, strength, print anisotropy as appropriate.
5. **Objective and constraints**: e.g. minimize compliance at a volume fraction, with specified tolerances.
6. **Solver plus interpretation**: solve the physics, reconstruct manufacturable geometry, validate it independently.

This repository handles only a designer-authored graph and implicit solid construction. It is a great place to learn the geometry infrastructure **before** attempting actual optimization.

## Suggested next software modules

A well-scoped extension would add `organic/keepouts.py` (component/connector envelopes), a FreeCAD datum-export contract, `organic/lattice.py` for selectable graph algorithms, a dimensioned bore inspector, and later an independent FEM solver integration. Don't fold unvalidated optimization claims into the shape generator.

The existing Blender script can stay a small, replaceable backend. That's one benefit of putting geometry code in ordinary Python rather than embedding every calculation in `bpy` scene logic.

Proceed to [the capstone project](CAPSTONE.md), where you'll take responsibility for the design graph and final evidence yourself.
