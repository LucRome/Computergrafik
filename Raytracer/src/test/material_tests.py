from unittest import TestCase
from raytracer.materials import Material
import numpy as np

class MaterialTests(TestCase):
    def test_constructor(self):
        [rgb, illu] = [np.array([255,255,255]), 100]
        m = Material(rgb, illu)
        self.assertTrue(np.equal(rgb, m.rgb).all())
        self.assertEqual(illu, m.illumination)
        [rgb, illu] = [np.array([0,0,0]), 100]
        m = Material(rgb, illu)
        self.assertTrue(np.equal(rgb, m.rgb).all())
        self.assertEqual(illu, m.illumination)
    
    def test_interpolation(self):
        [rgb1, illu1] = [np.array([255, 255, 255]), 90]
        [rgb2, illu2] = [np.array([255, 1, 1]), 11] # Overflow is tested
        [rgb_exp, illu_exp] = [np.array([255, 128, 128]), 100]
        a = Material(rgb1, illu1)
        b = Material(rgb2, illu2)
        c = a.interpolate(b)
        self.assertTrue(np.equal(rgb_exp, c.rgb).all())
        self.assertEqual(illu_exp, c.illumination)

    def test_travel(self):
        illu_start = 100
        [degrad, dis] = [0.1, 100]
        illu_exp = 90
        a = Material([0,0,0], illu_start)
        b= a.travel(dis, degrad)
        self.assertEqual(illu_exp, b.illumination)
    
    def test_return(self):
        mat = Material([240, 90, 4], 50)
        expected = [120, 45, 2]
        real = mat.to_rgb_array()
        self.assertTrue(np.equal(expected, real).all())