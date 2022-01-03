from numpy import float64, linalg
from numpy.lib.function_base import rot90
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
    width_half: float
    height_half: float
    depth_half: float
    bounding_sphere: Sphere
    # Surface Planes
    x_y_surfaces: List[Plane]
    x_z_surfaces: List[Plane]
    y_z_surfaces: List[Plane]
    # Rotation Matrix
    rotation_matrix: np.ndarray

    def __init__(self, rotation: float, width:float, height: float, depth: float, material: Material, offset_center: List[np.float64]) -> None:
        super().__init__(material, offset_center)
        self.height_half = height / 2
        self.width_half = width / 2
        self.depth_half = depth / 2
        radius = np.linalg.norm([self.width_half, self.height_half, self.depth_half])
        self.bounding_sphere = Sphere(radius, SHADOW_MATERIAL, offset_center)
        self.x_y_surfaces = list([
            Plane([width, 0, 0], [0, height, 0], np.add(offset_center, [0,0, -self.depth_half]), SHADOW_MATERIAL),
            Plane([width, 0, 0], [0, height, 0], np.add(offset_center, [0,0, self.depth_half]), SHADOW_MATERIAL)
        ])
        self.x_z_surfaces = list([
            Plane([width, 0, 0], [0, 0, depth], np.add(offset_center, [0, -self.height_half, 0]), SHADOW_MATERIAL),
            Plane([width, 0, 0], [0, 0, depth], np.add(offset_center, [0, self.height_half, 0]), SHADOW_MATERIAL)
        ])
        self.y_z_surfaces = list([
            Plane([0, height, 0], [0, 0, depth], np.add(offset_center, [-self.width_half, 0, 0]), SHADOW_MATERIAL),
            Plane([0, height, 0], [0, 0, depth], np.add(offset_center, [self.width_half, 0, 0]), SHADOW_MATERIAL)
        ])
        rot_rad = np.deg2rad(rotation)
        self.rotation_matrix = np.array([
            [np.cos(rot_rad), 0, -np.sin(rot_rad)],
            [0, 1, 0],
            [np.sin(rot_rad), 0, np.cos(rot_rad)]
        ])

    def get_intersection_params(self, ray: Ray):
        nearest_param: np.float64 = inf
        relative_offset_transformed =  np.dot(self.rotation_matrix, (ray.offset - self.offset))
        new_offset = relative_offset_transformed + self.offset
        new_direction =  np.dot(self.rotation_matrix, ray.direction)
        ray_transformed = Ray(new_offset, new_direction)

        if len(self.bounding_sphere.get_intersection_params(ray_transformed)) > 0:
            for plane in self.x_y_surfaces:
                params = plane.get_intersection_params(ray_transformed)
                if len(params) > 0 and params[0] < nearest_param:
                    x, y, z = ray_transformed.offset + params[0] * ray_transformed.direction - self.offset # Compute Intersect Point and bring it into the cubicle coordinate system
                    if x <= self.width_half and x >= -self.width_half and y <= self.height_half and y >= -self.height_half:
                        nearest_param = params[0]
            for plane in self.x_z_surfaces:
                params = plane.get_intersection_params(ray_transformed)
                if len(params) > 0 and params[0] < nearest_param:
                    x, y, z = ray_transformed.offset + params[0] * ray_transformed.direction - self.offset
                    if x <= self.width_half and x >= -self.width_half and z <= self.depth_half and z >= -self.depth_half:
                        nearest_param = params[0]
            for plane in self.y_z_surfaces:
                params = plane.get_intersection_params(ray_transformed)
                if len(params) > 0 and params[0] < nearest_param:
                    x, y, z = ray_transformed.offset + params[0] * ray_transformed.direction - self.offset
                    if y <= self.height_half and y >= -self.height_half and z <= self.depth_half and z >= -self.depth_half:
                        nearest_param = params[0]
            
            if nearest_param == inf:
                return []
            return [nearest_param]
        return []
    
    def get_normal(self, point: np.ndarray):
        x, y, z = point - self.offset
        if x == 0:
            return self.rotation_matrix * [-1, 0, 0]
        if x == self.width_half:
            return self.rotation_matrix * [1, 0, 0]
        if y == 0:
            return self.rotation_matrix * [0, -1, 0]
        if y == self.height_half:
            return self.rotation_matrix * [0, 1, 0]
        if z == 0:
            return self.rotation_matrix * [0, 0, -1]
        if z == self.depth_half:
            return self.rotation_matrix * [0, 0, 1]
            