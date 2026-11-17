"""Mathematical invariants for the core SDF vocabulary."""
import unittest
import numpy as np
from organic.fields import segment_distance, smooth_union, capped_cylinder_y, quadratic_bezier
from organic.field_lab import compute_fields


class FieldTests(unittest.TestCase):
    def test_capsule_end_and_midpoint(self):
        d = segment_distance(0, 0, 0, [-10, 0, 0], [10, 0, 0], 3, 3)
        self.assertAlmostEqual(float(d), -3.0)
        self.assertAlmostEqual(float(segment_distance(0, 0, 3, [-10, 0, 0], [10, 0, 0], 3, 3)), 0.0)
        self.assertAlmostEqual(float(segment_distance(0, 0, 5, [-10, 0, 0], [10, 0, 0], 3, 3)), 2.0)

    def test_taper(self):
        self.assertAlmostEqual(float(segment_distance(-10, 0, 0, [-10, 0, 0], [10, 0, 0], 4, 2)), -4)
        self.assertAlmostEqual(float(segment_distance(10, 0, 0, [-10, 0, 0], [10, 0, 0], 4, 2)), -2)

    def test_smooth_union_blends_but_hard_union_does_not(self):
        self.assertAlmostEqual(float(smooth_union(0, 0, 0)), 0)
        self.assertAlmostEqual(float(smooth_union(0, 0, 4)), -1.0)
        self.assertAlmostEqual(float(smooth_union(-4, 10, 4)), -4)

    def test_drilled_cylinder_y(self):
        boss = capped_cylinder_y(0, 0, 0, [0, 0, 0], 10, 8)
        bore = capped_cylinder_y(0, 0, 0, [0, 0, 0], 3, 20)
        self.assertGreater(float(np.maximum(boss, -bore)), 0)
        edge = capped_cylinder_y(10, 0, 0, [0, 0, 0], 10, 8)
        self.assertAlmostEqual(float(edge), 0)

    def test_bezier_control_point(self):
        p0, pc, p1 = [0, 0, 0], [10, 0, 20], [20, 0, 0]
        self.assertEqual(quadratic_bezier(p0, pc, p1, 0), p0)
        self.assertEqual(quadratic_bezier(p0, pc, p1, 1), p1)
        self.assertAlmostEqual(quadratic_bezier(p0, pc, p1, .5)[2], 10.0)

    def test_visualization_fields_have_both_air_and_solid(self):
        _, _, fs = compute_fields()
        for field in fs:
            self.assertLess(float(np.min(field)), 0)
            self.assertGreater(float(np.max(field)), 0)


if __name__ == '__main__':
    unittest.main()
