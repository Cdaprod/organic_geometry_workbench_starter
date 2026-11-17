# Learning path — From first sphere to organic camera arm

This is the course index for readers who want to **understand the shape**, not merely obtain its STL. The [README](README.md) is the walk-through; these chapters explain the mathematics, decisions, and experiments at greater depth.

**Preparation:** Python 3.10+, `python -m pip install -e .` in a virtual environment. All shape code is ordinary Python/NumPy; Blender is optional.

| Order | Read | Do | Explain before continuing |
|---|---|---|---|
| 0 | [README](README.md) | Generate `first_arm.json` | What is an SDF's zero level-set? |
| 1 | [Coordinate frames](docs/01-coordinate-frames.md) | Draw a mount/strut graph | Why is Y the bore axis? |
| 2 | [Distance fields](docs/02-distance-fields.md) | Run `organic.field_lab` | How does a radius turn a segment into a solid? |
| 3 | [Curves and branches](docs/03-curves-and-branches.md) | Change one control point | How is curved centerline sampling different from grid resolution? |
| 4 | [Mounts and holes](docs/04-constraints-and-holes.md) | Modify a hole radius | Why are holes subtracted after the smooth unions? |
| 5 | [Meshing and verification](docs/05-mesh-and-verification.md) | Compare voxel resolutions | Why doesn't watertight mean safe? |
| 6 | [Blender and engineering](docs/06-blender-and-engineering.md) | Render the STL | Which part is Python math versus Blender presentation? |
| 7 | [Capstone](docs/CAPSTONE.md) | Build a distinct arm | Can you justify all features and provide an honest verification report? |

There are no hidden generators: study `organic/fields.py` for the equations and `organic/build.py` for the process that turns them into an STL. The chapter explanations are paired with [working SVG diagrams](docs/figures/sdf_operations.svg) and real mesh renders.
