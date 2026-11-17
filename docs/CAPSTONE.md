# Capstone — Design your own organic monitor or camera arm

**The test isn't whether you can generate a nice image. It's whether you can explain what produced it and reproduce the result from source.**

## The brief

Design an original two-mount organic arm inspired by a camera or monitor rig. Use **invented illustrative dimensions** initially — do not claim it fits a real camera without measuring the hardware.

Requirements for your learning model:

- Two independent mounting centers with an explicitly stated axis convention.
- At least three intermediate design nodes and two different branches between mounts.
- At least one quadratic Bézier strut and one visibly tapered strut.
- Two protected nominal bores that remain clear after blending.
- Reproducible JSON source, an STL, real geometry preview, and a validation report.
- A written explanation of what one parameter change did and why.

## Method — six concrete decisions

### 1. Write the coordinate contract

Pick `base=[0,0,0]`; choose a tip X/Z location in millimeters. Remember the bore axis in this starter is **Y**. Note the *actual* center distance, not just the X distance.

### 2. Sketch the graph first

Draw two or more routes connecting the mounting bosses. Give your nodes names with meaning: `base`, `upper`, `lower`, `mid`, `tip`. If you cannot explain why an edge connects two nodes, remove or justify it.

### 3. Declare what stays fixed

Keep mounting coordinates and nominal hole dimensions unchanged during the first experiments. Only move control points and strut radii. This isolates the cause of geometric changes.

### 4. Write a distinct JSON specification

Copy `examples/first_arm.json`, rename its `name` to a unique slug, then edit the node graph. Reusing the *engine* is the goal; reusing its exact arm graph is not. Keep your units in millimeters and place control points within your chosen coordinate system.

### 5. Build, inspect, iterate

Run:

```bash
python -m organic.build examples/my_arm.json
python -m organic.field_lab --out results/field_lab.png
python -m unittest discover -s tests -v
```

Use the actual output paths generated for your chosen `name`. Inspect the section image for bores, intersections and walls. If something breaks, explain it in terms of the field equations rather than editing the STL manually.

### 6. Create an honest engineering note

Your final README section should include:

| Evidence | What you should report |
|---|---|
| Geometry screenshot | Actual generated model with a reproducible camera/view |
| Design data | JSON filename, coordinate frame and node/mount table |
| Mesh validation | Watertight, winding, component count, volume, bounds and voxel size |
| Functional limits | Nominal bores but actual fit unverified; physical dimensions needing measurement |
| Structural limits | Loads, materials, FEA and fatigue **not** verified |
| Iteration | What you changed, what you predicted and what actually happened |

## Self-assessment (write answers before opening the solution)

1. At the center of an SDF sphere with radius 6 mm, what value does the function return?
2. If `blend_mm` changes from 0 to 4, is the change applied at all vertices after meshing or to the field before meshing?
3. If the mount's nominal hole radius increases, does that prove a larger real bolt will fit the eventual printed part?
4. If the camera tip moves from `[80,0,20]` to `[80,0,30]`, what changes and what does not necessarily change?
5. If volume decreases 18%, how much did stiffness increase?

<details><summary>Reveal the answer key</summary>

1. `-6 mm` (negative means inside the sphere).
2. It changes the smooth field union **before** extracting the surface; it does not apply a post-mesh modifier.
3. No. It changes nominal geometry, while voxel resolution, process tolerance and printed fit still require inspection.
4. Its position and paths connected to it move; any unrelated nodes may stay fixed. The actual length between pivot centers changes and must be recalculated.
5. Unknown. Volume alone does not determine stiffness, and may decrease it for the same loads and constraints.

</details>

## Stretch goal: separate shape generation from optimization

Define a *hypothetical* force vector at the camera tip and a fixed base. Write down which information a finite element solver would still need: material, boundary conditions, load direction, geometry fidelity and allowable stress/displacement. **Do not claim the generated struts follow optimal stress trajectories** until you've actually solved and checked that engineering problem.

If you've completed the brief, you can now make a new organic procedural structure from coordinates and constraints, explain its main equations, and supply reproducible evidence. That's the meaningful endpoint of this starter curriculum.
