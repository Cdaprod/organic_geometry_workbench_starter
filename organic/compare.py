"""Compare two design specifications without pretending volume means strength.

Run: python -m organic.compare examples/first_arm.json examples/camera_arm.json
"""
import argparse
import json
from pathlib import Path

from .build import generate


def describe(spec_path):
    spec = json.loads(Path(spec_path).read_text())
    mesh = generate(spec)
    return {
        'file': str(spec_path),
        'design': spec['name'],
        'voxel_mm': spec['voxel_mm'],
        'volume_mm3': float(mesh.volume),
        'components': len(mesh.split(only_watertight=False)),
        'watertight': bool(mesh.is_watertight),
        'bounds_mm': mesh.bounds.tolist(),
        'faces': len(mesh.faces),
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('baseline', type=Path)
    p.add_argument('revision', type=Path)
    p.add_argument('--out', type=Path, default=Path('results/design_comparison.json'))
    args = p.parse_args()
    a, b = describe(args.baseline), describe(args.revision)
    result = {
        'baseline': a, 'revision': b,
        'volume_change_percent': 100 * (b['volume_mm3'] - a['volume_mm3']) / a['volume_mm3'],
        'warning': 'Volume comparison is NOT a load, stiffness, fatigue, or printability assessment. Compare matching mounting datums and same voxel resolution.',
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
