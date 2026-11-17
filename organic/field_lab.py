"""Visual explanation of implicit solids in a Y=0 cross-section.

Run: python -m organic.field_lab --out results/field_lab.png
Every plotted contour is computed using the SAME field primitives as the STL engine.
"""
import argparse
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from .fields import segment_distance, smooth_union, capped_cylinder_y


def sphere_sdf(x, z, cx, cz, radius):
    """Distance to the surface of a circle in a two-dimensional section."""
    return np.hypot(x - cx, z - cz) - radius


def compute_fields():
    x = np.linspace(-32, 32, 260)
    z = np.linspace(-25, 28, 220)
    X, Z = np.meshgrid(x, z)
    Y = np.zeros_like(X)
    sphere = sphere_sdf(X, Z, -11, -4, 11)
    first = segment_distance(X, Y, Z, [-22, 0, -13], [13, 0, 14], 5, 3)
    second = segment_distance(X, Y, Z, [-10, 0, 14], [24, 0, -11], 4, 5)
    hard = np.minimum(first, second)
    smooth = smooth_union(first, second, 5.0)
    boss = capped_cylinder_y(X, Y, Z, [0, 0, 0], 13, 12)
    bore = capped_cylinder_y(X, Y, Z, [0, 0, 0], 5, 32)
    drilled = np.maximum(boss, -bore)
    return x, z, [sphere, first, hard, smooth, drilled]


def render(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    x, z, fields = compute_fields()
    titles = [
        '1 · Sphere: distance - radius',
        '2 · Swept sphere: capsule/taper',
        '3 · Hard union: min(d1, d2)',
        '4 · Smooth union: rounded junction',
        '5 · Drill: max(boss, -bore)',
    ]
    fig, axes = plt.subplots(2, 3, figsize=(13.8, 8.4), dpi=145, constrained_layout=True)
    fig.patch.set_facecolor('#f6f8fa')
    for i, (ax, field, name) in enumerate(zip(axes.flat, fields, titles)):
        ax.set_facecolor('#eef4f8')
        field = np.asarray(field)
        ax.contourf(x, z, field, levels=[-100, 0, 100], colors=['#5b879d', '#edf3f6'])
        ax.contour(x, z, field, levels=[0], colors=['#15374a'], linewidths=2.0)
        ax.set_title(name, fontsize=11, weight='bold', pad=9)
        ax.set_xlabel('X (mm)')
        ax.set_ylabel('Z (mm)')
        ax.set_aspect('equal')
        ax.grid(alpha=0.10)
    axes.flat[-1].axis('off')
    axes.flat[-1].text(.05, .75, 'BLUE = negative field (solid)\nWHITE = positive field (air)\nDARK OUTLINE = field = 0', fontsize=13, transform=axes.flat[-1].transAxes, linespacing=2)
    axes.flat[-1].text(.05, .36, 'Compare panels 3 and 4: \nblending adds a smooth junction.\nPanel 5 preserves the bore as a hard cut.', fontsize=11, transform=axes.flat[-1].transAxes, linespacing=1.7)
    fig.suptitle('One mathematical language, five geometry operations', weight='bold', fontsize=18)
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    return path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', type=Path, default=Path('results/field_lab.png'))
    args = p.parse_args()
    print('Wrote', render(args.out))


if __name__ == '__main__':
    main()
