import numpy
from raytracer.coordinate_utils import Ray, is_normalised, normalise
import unittest
import numpy as np

class CoordinateUtilsTests(unittest.TestCase):
    def test_cu(self):
        vec1 = np.array([1,2,3], dtype=np.float64)
        vec1 = normalise(vec1)

        self.assertEqual(np.linalg.norm(vec1), 1)
        self.assertTrue(is_normalised(vec1))

        [off, dir] = [np.array([0,0,-2], dtype=np.float64), np.array([2,4,-10], dtype=np.float64)]
        ray = Ray(off, dir)
        self.assertTrue(np.equal(ray.offset, off).all())
        self.assertTrue(is_normalised(ray.direction))