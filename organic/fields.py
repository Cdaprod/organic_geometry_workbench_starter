"""Small, reusable signed-distance geometry functions, in millimetres.

Sign convention: negative = inside solid, positive = outside.
All functions broadcast over NumPy arrays.
"""
import numpy as np


def smooth_union(a, b, blend_mm):
    """Soft union between two signed-distance fields (approximate SDF)."""
    if blend_mm <= 0:
        return np.minimum(a, b)
    h = np.clip(0.5 + 0.5 * (b - a) / blend_mm, 0.0, 1.0)
    return b * (1.0 - h) + a * h - blend_mm * h * (1.0 - h)


def segment_distance(x, y, z, p, q, radius_start, radius_end):
    """A tapered, capped strut between arbitrary 3D endpoints."""
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    v = q - p
    t = np.clip(((x - p[0]) * v[0] + (y - p[1]) * v[1]
                 + (z - p[2]) * v[2]) / max(float(v @ v), 1e-9), 0.0, 1.0)
    r = radius_start + t * (radius_end - radius_start)
    return np.sqrt((x - p[0] - t * v[0]) ** 2
                   + (y - p[1] - t * v[1]) ** 2
                   + (z - p[2] - t * v[2]) ** 2) - r


def capped_cylinder_y(x, y, z, center, radius, width):
    """Finite cylindrical boss or drill envelope whose bore axis is Y."""
    cx, cy, cz = center
    a = np.sqrt((x - cx) ** 2 + (z - cz) ** 2) - radius
    b = np.abs(y - cy) - width / 2.0
    return np.sqrt(np.maximum(a, 0) ** 2 + np.maximum(b, 0) ** 2) + np.minimum(np.maximum(a, b), 0)


def quadratic_bezier(p0, control, p1, t):
    p0, control, p1 = (np.asarray(p, dtype=float) for p in (p0, control, p1))
    return ((1.0-t)**2*p0 + 2*(1.0-t)*t*control + t*t*p1).tolist()
