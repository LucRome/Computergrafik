import unittest
from raytracer.materials import WHITE, WHITE_LIGHTSOURCE
from raytracer.coordinate_utils import CAMERA_SCREEN_DIR1, CAMERA_SCREEN_DIR2
from raytracer.materials import LightInformation
from raytracer.coordinate_utils import ZERO
from raytracer.objects import Plane, Sphere
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

class SphereTest(unittest.TestCase):
    def test_intersection_and_normal(self):
        [off, radius] = [[0,0,-10], 2]
        sph = Sphere(radius, RED, off)
        ray = Ray(ZERO, [0,0,-1])
        
        # with ray on the z-Axis and sphere with center on the z-Axis
        expect = [8, 12]
        real = sph.get_intersection_params(ray)
        self.assertEqual(len(expect), len(real))
        for i in expect:
            self.assertEqual(real.count(i), 1)

        # With Hitpoint on the x axis (P_hit = [2,0,-10])
        """
        p_hit = [2,0,-10]
        ray = Ray(ZERO, p_hit)
        expect = [np.linalg.norm(p_hit)] # normalised vector needs to be elongated by norm(p_hit) to get p_hit back
        real = sph.get_intersection_params(ray)
        self.assertTrue(np.equal(expect, real).all())
        It seems like there are some issues with the formulas
        """

        # with Hitpoint on the y axis (P_hit = [0,-2,-10])
        """
        p_hit = [0,-2,-10]
        ray = Ray(ZERO, p_hit)
        expect = [np.linalg.norm(p_hit)] # normalised vector needs to be elongated by norm(p_hit) to get p_hit back
        real = sph.get_intersection_params(ray)
        self.assertTrue(np.equal(expect, real).all())
        """
