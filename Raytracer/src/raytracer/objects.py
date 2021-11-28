from raytracer.coordinate_utils import normalise, Ray
from raytracer.materials import Material

from typing import List
import numpy as np
"""
The Classes representing the Objects in the 3D Space
"""

def sign(x):
    return -1 if x < 0 else 1
class Object:
    material: Material
    offset: np.ndarray
    is_source: bool

    def __init__(self, material: Material, offset: List[np.float64]) -> None:
        self.material = material
        self.offset = np.array(offset, dtype=np.float64)
        self.is_source = (material.illumination > 0)
    
    def get_intersection_params(self, ray: Ray):
        pass

    def get_normal(self, point: np.ndarray):
        pass

class Plane(Object):
    normal: np.ndarray

    def __init__(self, vec1: List[np.float64], vec2: List[np.float64], offset: np.ndarray, 
        material: Material) -> None:
        super().__init__(material, offset)
        self.normal = normalise(np.array(np.cross(vec1, vec2), dtype=np.float64))

    def get_intersection_params(self, ray: Ray) -> List[np.float64]:
        ln = np.dot(ray.direction, self.normal)
        if np.abs(ln) < 1e-6:
            return [] # nearly parrallel -> no Intersect Point
        else:
            return [np.divide(np.dot(self.offset - ray.offset, self.normal), ln)]
        
    def get_normal(self, point: np.ndarray):
        return self.normal

"TODO: Tests"
class Sphere(Object):
    radius: np.float64
    
    def __init__(self, radius: np.float64, material: Material, offset: List[np.float64]) -> None:
        super().__init__(material, offset)
        self.radius = radius

    def get_intersection_params(self, ray: Ray):
        a = 1 # Rays are normalised
        b = np.multiply(2, np.dot(ray.direction, np.subtract(ray.offset, self.offset)))
        c = np.subtract(np.square(np.linalg.norm(np.subtract(ray.offset, self.offset))), np.square(self.radius))

        discriminant = np.subtract(np.square(b), np.multiply(4, np.multiply(a, c)))
        if discriminant < 0:
            return []
        else:
            q = - np.multiply(0.5, np.add(b, np.multiply(sign(b), np.sqrt(discriminant))))
            if discriminant == 0:
                return [np.divide(q, a)]
            else:
                return [np.divide(q,a), np.divide(c,q)]
    
    def get_normal(self, point: np.ndarray):
        return normalise(point - self.offset)
            
class LightSphere(Sphere):
    
    def __init__(self, radius: np.float64, rgb_color: List[np.int8], offset: List[np.float64]) -> None:
        super().__init__(radius, Material(rgb_color, 100), offset)
