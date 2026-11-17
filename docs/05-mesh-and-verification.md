# 05 — How an equation turns into a mesh (and where artifacts come from)

You now have a function that describes a solid at any point. An STL, however, needs triangles. This is the job of **sampling** and **isosurface extraction**.

## The 3D sampling grid

`organic/build.py` finds a bounding volume that contains the nodes, control points and mount radii with a margin. Then it makes regularly spaced sample coordinates:

```python
axes = [np.arange(low[k], high[k] + step, step) for k in range(3)]
x, y, z = np.meshgrid(*axes, indexing='ij', sparse=True)
```

The actual implementation includes array-size protection. The sparse coordinate grids are broadcast through the distance equations; the final accumulated solid field is a dense 3D array.

If a bounding box measures 100 × 50 × 50 mm and `voxel_mm=1`, that's roughly 250,000 field samples (before end padding). At half the spacing there are roughly **eight times as many** samples. Reducing the voxel size isn't free.

## Marching cubes finds the `d=0` surface

The engine calls `skimage.measure.marching_cubes(field, level=0, ...)` to triangulate where nearby samples cross the surface. That mesh is handed to `trimesh` for export, normals and basic checks.

An SDF isn't itself a triangle mesh. Marching cubes also doesn't know which hole was *supposed* to be 7.000 mm — it only interpolates a sampled field. Rounding at the voxel scale is a normal consequence.

## An experiment that will teach you more than five tutorials

Create `examples/my_first_arm.json` and keep every design parameter constant except `voxel_mm`:

| Run | `voxel_mm` | Hypothesis |
|---|---:|---|
| A | 2.0 | Fast and visibly coarse, possibly distorts small holes |
| B | 1.2 | Baseline from the course |
| C | 0.7 | More detail, greater memory/time cost |

Generate each under a distinct `name` (for example, `arm_2mm`, `arm_12mm`, `arm_07mm`), so reports and renders remain available. Compare `vertex_count`, `face_count`, mesh bounds, and mesh volume in each `validation.json`.

Try to explain *why* facet count changed. If the model becomes more detailed, does that prove it is dimensionally correct? **No.** You'll still need to check real dimensional targets and print tolerances.

## What the validator actually checks

The current report includes watertightness, winding consistency, component count, volume, bounds, and triangle counts. These catch useful geometric errors but are **not** production certifications.

A mesh can be watertight and still have thin bridges, intersect a cable, be difficult to print, or fail under a load. A closed mesh is necessary for many fabrication workflows, but it isn't sufficient.

The included tests exercise field math and a connected watertight example. They do not perform finite element analysis, determine structural safety, or validate physical connector fit.

## Debugging shapes with a section

`organic/preview.py` makes a section through `Y=0`, then renders actual mesh triangles. This is especially useful for checking whether a bore is open, whether material merged as intended, and whether a branch intersects the intended region.

**Rigor checkpoint:** If a narrow beam is missing, check the graph endpoints, field sign, voxel resolution, and whether the beam intersects the union. Don't immediately apply global mesh smoothing and hope the shape repairs itself.

Next: [06 — Blender and the engineering boundary](06-blender-and-engineering.md).
