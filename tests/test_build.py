"""Integration check: the learning example must build a usable single mesh."""
import json
from pathlib import Path
import unittest

from organic.build import generate, validate_spec

ROOT = Path(__file__).resolve().parents[1]


class BuildTests(unittest.TestCase):
    def test_invalid_strut_rejected(self):
        cfg = json.loads((ROOT / 'examples/first_arm.json').read_text())
        cfg['struts'][0]['b'] = 'missing'
        with self.assertRaises(ValueError):
            validate_spec(cfg)

    def test_first_arm_watertight(self):
        cfg = json.loads((ROOT / 'examples/first_arm.json').read_text())
        cfg['voxel_mm'] = 1.6  # lightweight CI geometry; tutorial defaults are finer
        mesh = generate(cfg)
        self.assertTrue(mesh.is_watertight)
        self.assertTrue(mesh.is_winding_consistent)
        self.assertEqual(len(mesh.split(only_watertight=False)), 1)
        self.assertGreater(mesh.volume, 0)


if __name__ == '__main__':
    unittest.main()
