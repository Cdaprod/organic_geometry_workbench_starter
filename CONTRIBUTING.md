# Contributing to the workbench

The most valuable contribution is one a newcomer can **learn from and reproduce**. New primitives should come with (1) the mathematical sign convention, (2) a unit test at an inside, surface and outside point, (3) an exercise showing what a parameter changes, (4) a geometry-derived preview, and (5) a clear boundary between verified behavior and engineering assumptions.

Use millimeters; keep user design data in `examples/*.json` rather than hard-coding it into a new generator; add reusable math in `organic/fields.py` or another narrowly focused module. Do not describe a shape as topology-optimized unless the implementation includes physics-based optimization and independent validation.

Run before contributing:

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m organic.build examples/first_arm.json
python -m organic.field_lab --out results/field_lab.png
```

Avoid committing generated temporary build caches or local virtual environments. Existing preview PNGs and educational diagrams are tracked intentionally for GitHub readers.
