# Troubleshooting — when an experiment doesn't behave as expected

## `No module named organic`

Run Python from the repository root and install the package in your active environment: `python -m pip install -e .`. Check `which python` on macOS/Linux or `Get-Command python` on PowerShell.

## The build consumes too much memory or takes too long

Increase `voxel_mm` in your JSON to something like 1.5 or 2.0 for a draft. Each halving of the step can increase the sample count by about 8×. The engine also rejects grids above 16 million cells.

## A strut disappears

Check its node names, endpoint coordinates, radii and whether it joins any other solid. A strut thinner than the voxel spacing can be lost by sampling. Try a coarser *design* with thicker features first, then refine the sampling resolution.

## My output is multiple disconnected meshes

A graph edge may be disconnected in coordinates even if the JSON graph looks connected; Boolean and grid behavior matter. Check that struts physically overlap mounts/other branches, not just meet at a nominal point on an insufficient grid.

## The hole isn't a perfect circle

The source defines a circular nominal bore, but marching cubes creates triangles from sampled data. Try a smaller `voxel_mm`, and measure actual exported geometry. A lower voxel value isn't a substitute for tolerance design or a precise CAD bore when engineering fit matters.

## Blender import or render fails

The STL engine and its `preview.png` don't need Blender. First confirm `results/<name>/<name>.stl` exists and the generator's validation completed. Then check your executable path and Blender version. The import script supports the 4.x STL operator with a fallback for older versions.

## An STL is watertight, but the model still looks wrong

Watertightness means the surface closes. It doesn't prove the shape matches your design. Compare cross sections, mounting datums, hole dimensions and graph inputs; don't treat a pretty render as mechanical acceptance.

## How to report a useful bug

Include the exact JSON specification, Python version, dependency versions, command used, error traceback, `validation.json`, the generated preview, and a short sentence describing **expected vs observed geometry**. Never post private credentials or identifying hardware network configuration in a bug report.
