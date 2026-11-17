# Figure provenance

The repository's `previews/camera_arm.png` and `previews/triangular_bracket.png` are renders of actual generated meshes and middle cross-sections. They are not AI images or FEA stress maps.

`docs/figures/arm_graph.svg` is a diagram of the exact node and strut data in `examples/first_arm.json` (the design skeleton, not the exported triangle mesh). `docs/figures/sdf_operations.svg` traces the zero level-set of field functions from `organic/fields.py` using a Y=0 section. It is a mathematical visualization, not a manufactured-part verification.

`python -m organic.field_lab --out results/field_lab.png` regenerates a more detailed five-panel figure from those same distance-field primitives. `python -m organic.build examples/first_arm.json` generates its own geometry-derived STL and PNG preview. The generated numerical reports document sampled mesh properties only.
