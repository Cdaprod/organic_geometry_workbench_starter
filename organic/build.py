#!/usr/bin/env python3
"""Build a reproducible, topology-INspired (not FEA-optimized) organic lattice.

Usage: python -m organic.build examples/camera_arm.json
Requires: numpy, scikit-image, trimesh, matplotlib.
"""
import argparse
import json
from pathlib import Path
import numpy as np
import trimesh
from skimage.measure import marching_cubes
from .fields import smooth_union, segment_distance, capped_cylinder_y, quadratic_bezier


def validate_spec(config):
    nodes = config['nodes']
    if len(nodes) < 2 or not config['struts'] or not config['mounts']:
        raise ValueError('Need at least two nodes, a strut, and a mount')
    if float(config['voxel_mm']) <= 0 or float(config.get('blend_mm', 1.0)) < 0:
        raise ValueError('voxel_mm must be positive; blend_mm cannot be negative')
    for key, v in nodes.items():
        if len(v) != 3 or not all(np.isfinite(v)):
            raise ValueError(f'Invalid 3D node: {key}')
    for edge in config['struts']:
        if edge['a'] not in nodes or edge['b'] not in nodes:
            raise ValueError('Strut references missing node')
        if min(edge.get('radius_a_mm', 0), edge.get('radius_b_mm', 0)) <= 0:
            raise ValueError('Strut radii must be positive')
    for mount in config['mounts']:
        if mount['node'] not in nodes:
            raise ValueError('Mount references missing node')
        if not (0 < mount['hole_radius_mm'] < mount['outer_radius_mm']):
            raise ValueError('Mount hole must be smaller than outer radius')
        if mount.get('axis', 'Y') != 'Y':
            raise ValueError('This starter currently supports Y-axis mounting holes only')


def make_grid(config):
    points = [np.array(v, dtype=float) for v in config['nodes'].values()]
    points += [np.array(s['control'], dtype=float) for s in config['struts'] if 'control' in s]
    a = np.min(points, axis=0)
    b = np.max(points, axis=0)
    margin = max([float(m['outer_radius_mm']) for m in config['mounts']] +
                 [float(s['radius_a_mm']) for s in config['struts']] +
                 [float(s['radius_b_mm']) for s in config['struts']]) + 5.0
    a -= margin
    b += margin
    step = float(config['voxel_mm'])
    # Avoid arbitrary array expansion: exactly one explicit resolution control.
    axes = [np.arange(a[k], b[k] + step * 1.01, step, dtype=np.float32) for k in range(3)]
    count = np.prod([len(axis) for axis in axes])
    if count > 16_000_000:
        raise ValueError('Grid >16M cells; increase voxel_mm or reduce dimensions')
    x, y, z = np.meshgrid(*axes, indexing='ij', sparse=True)
    return (x, y, z), axes


def generate(config):
    validate_spec(config)
    (x, y, z), axes = make_grid(config)
    shape = np.full(tuple(len(a) for a in axes), 1e5, dtype=np.float32)
    k = float(config.get('blend_mm', 1.0))
    nodes = config['nodes']
    for item in config['struts']:
        a, b = nodes[item['a']], nodes[item['b']]
        n = max(2, int(item.get('samples', 9)))
        if 'control' in item:
            pts = [quadratic_bezier(a, item['control'], b, t) for t in np.linspace(0, 1, n)]
        else:
            pts = [a, b]
        for j in range(len(pts)-1):
            u, v = j/(len(pts)-1), (j+1)/(len(pts)-1)
            ra = float(item['radius_a_mm']); rb = float(item['radius_b_mm'])
            field = segment_distance(x, y, z, pts[j], pts[j+1],
                                     ra+(rb-ra)*u, ra+(rb-ra)*v)
            shape = smooth_union(shape, field, k).astype(np.float32)
    # Add mount bosses before drilling. This preserves bolt access in the final mesh.
    for mount in config['mounts']:
        p = nodes[mount['node']]
        boss = capped_cylinder_y(x, y, z, p,
                                 mount['outer_radius_mm'], mount['width_mm'])
        shape = smooth_union(shape, boss, k).astype(np.float32)
    # Holes are hard exclusions; do not smooth them back into solid material.
    for mount in config['mounts']:
        p = nodes[mount['node']]
        drill = capped_cylinder_y(x, y, z, p,
                                  mount['hole_radius_mm'], mount['width_mm'] + 20.0)
        shape = np.maximum(shape, -drill).astype(np.float32)
    vertices, faces, _, _ = marching_cubes(shape, level=0.0,
                                            spacing=(float(config['voxel_mm']),)*3,
                                            allow_degenerate=False)
    vertices += np.array([a[0] for a in axes])
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=True)
    mesh.fix_normals()
    return mesh


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('spec', type=Path, help='JSON design specification')
    cli.add_argument('--out', type=Path, default=Path('results'))
    args = cli.parse_args()
    spec = json.loads(args.spec.read_text())
    mesh = generate(spec)
    out = args.out / spec['name']
    out.mkdir(parents=True, exist_ok=True)
    mesh.export(out / (spec['name'] + '.stl'))
    report = {'name': spec['name'], 'voxel_mm': spec['voxel_mm'],
              'watertight': bool(mesh.is_watertight),
              'winding_consistent': bool(mesh.is_winding_consistent),
              'components': int(len(mesh.split(only_watertight=False))),
              'volume_mm3': float(mesh.volume),
              'bounds_mm': mesh.bounds.tolist(),
              'vertex_count': len(mesh.vertices), 'face_count': len(mesh.faces),
              'limitations': ['Topology-inspired shape, NOT stress-optimized or FEA verified',
                              'Clearance, hole-fit, load rating and printability unverified']}
    (out/'validation.json').write_text(json.dumps(report, indent=2)+'\n')
    from .preview import preview
    preview(mesh, spec, out / 'preview.png')
    print(json.dumps({'stl': str(out / (spec['name'] + '.stl')),
                      'preview': str(out / 'preview.png'), **report}, indent=2))


if __name__ == '__main__':
    main()
