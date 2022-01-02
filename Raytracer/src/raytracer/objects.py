from numpy import linalg
from raytracer.coordinate_utils import normalise, Ray
from raytracer.materials import Material, SHADOW_MATERIAL

from math import inf
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
            return [np.dot(self.offset - ray.offset, self.normal) / ln]
        
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
        b = 2 * np.dot(ray.direction, (ray.offset - self.offset))
        c = np.square(np.linalg.norm(ray.offset - self.offset)) - np.square(self.radius)

        discriminant = np.square(b) - (4 * a * c)
        if discriminant < 0:
            return []
        else:
            q = - 0.5 * (b + (sign(b) * np.sqrt(discriminant)))
            if discriminant == 0:
                return [(q / a)]
            else:
                return [(q/a), (c/q)]
    
    def get_normal(self, point: np.ndarray):
        return normalise(point - self.offset)
            
class LightSphere(Sphere):
    
    def __init__(self, radius: np.float64, rgb_color: List[np.int8], offset: List[np.float64]) -> None:
        super().__init__(radius, Material(rgb_color, 100), offset)


class CuboidVertical(Object):
    """
    Represents a cuboid, with it's height always in the y-direction
    """
    x_max: float
    y_max: float
    z_max: float
    bounding_sphere: Sphere
    # Surface Planes
    x_y_surfaces: List[Plane]
    x_z_surfaces: List[Plane]
    y_z_surfaces: List[Plane]

    def __init__(self, width:float, height: float, depth: float, material: Material, offset: List[np.float64]) -> None:
        super().__init__(material, offset)
        self.y_max = height
        self.x_max = width
        self.z_max = depth
        radius = max([width, height, depth])
        self.bounding_sphere = Sphere(radius, SHADOW_MATERIAL, offset)
        self.x_y_surfaces = list(
            Plane([width, 0, 0], [0, height, 0], offset, SHADOW_MATERIAL),
            Plane([width, 0, 0], [0, height, 0], (offset + [0,0,depth]), SHADOW_MATERIAL)
        )
        self.x_z_surfaces = list(
            Plane([width, 0, 0], [0, 0, depth], offset, SHADOW_MATERIAL),
            Plane([width, 0, 0], [0, 0, depth], (offset + [0, height, 0]), SHADOW_MATERIAL)
        )
        self.y_z_surfaces = list(
            Plane([0, height, 0], [0, 0, depth], offset, SHADOW_MATERIAL),
            Plane([0, height, 0], [0, 0, depth], (offset + [width, 0, 0]), SHADOW_MATERIAL)
        )

    def get_intersection_params(self, ray: Ray):
        if len(self.bounding_sphere.get_intersection_params()) > 0:
            nearest_param: np.float64 = inf

            for plane in self.x_y_surfaces:
                params = plane.get_intersection_params()
                if len(params) > 0 and params[0] < nearest_param:
                    intersect_point = ray.offset + params[0] * ray.direction - self.offset # Compute Intersect Point and bring it into the cubicle coordinate system
                    if intersect_point[0] <= self.x_max and intersect_point[1] <= self.y_max:
                        nearest_param = params[0]
            for plane in self.x_z_surfaces:
                params = plane.get_intersection_params()
                if len(params) > 0 and params[0] < nearest_param:
                    intersect_point = ray.offset + params[0] * ray.direction - self.offset
                    if intersect_point[0] <= self.x_max and intersect_point[2] <= self.z_max:
                        nearest_param = params[0]
            for plane in self.y_z_surfaces:
                params = plane.get_intersection_params()
                if len(params) > 0 and params[0] < nearest_param:
                    intersect_point = ray.offset + params[0] * ray.direction - self.offset
                    if intersect_point[1] <= self.y_max and intersect_point[2] <= self.z_max:
                        nearest_param = params[0]
            
            return nearest_param
        return []
    
    def get_normal(self, point: np.ndarray):
        x, y, z = point - self.offset
        if x == 0 or x == self.x_max:
            