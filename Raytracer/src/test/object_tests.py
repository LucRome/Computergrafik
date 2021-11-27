import unittest
from raytracer.materials import WHITE, WHITE_LIGHTSOURCE
from raytracer.coordinate_utils import CAMERA_SCREEN_DIR1, CAMERA_SCREEN_DIR2
from raytracer.materials import Material
from raytracer.coordinate_utils import ZERO
from raytracer.objects import Plane
from raytracer.coordinate_utils import Ray
from raytracer.materials import RED

import numpy as np

import unittest

class PlaneTests(unittest.TestCase):
    def test_constructor(self):
        [off, vec1, vec2, mat1, mat2] = [ZERO, CAMERA_SCREEN_DIR1, CAMERA_SCREEN_DIR2, WHITE_LIGHTSOURCE, WHITE]
        p = Plane(vec1, vec2, off, mat1)
        normal_exp = [0,0,1]
        self.assertTrue(np.equal(p.get_normal(ZERO), normal_exp).all())
        self.assertTrue(p.is_source)
        p = Plane(vec1, vec2, off, mat2)
        self.assertFalse(p.is_source)

    def test_intersection(self):
        # simple intersect points
        p = Plane([1,0,0],[0,1,0], [0,0,-10], RED)
        ray = Ray([0,0,0],[0,0,-1])

        params = p.get_intersection_params(ray)
        self.assertEqual(params[0], 10)

        # parallel ray
        ray = Ray([0,0,0], [1,0,0]) 
        params = p.get_intersection_params(ray)
        self.assertEqual(len(params), 0)