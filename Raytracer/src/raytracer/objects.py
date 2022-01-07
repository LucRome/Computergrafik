from numpy import float64, linalg
from .light_sources import LightSource, PointLight
from .coordinate_utils import normalise, Ray

from .light_utils import BLACK, Light

from math import inf
from typing import List, Optional, Tuple
import numpy as np



"""
The Classes representing the Objects in the 3D Space
"""

def sign(x):
    return -1 if x < 0 else 1

class Object:
    """
    Generic Interface for a Object in 3D Space
    contains
     - albedo: Color of Object
     - offset: Position of Object
     - source_object: Optional Object representing a light source
    """
    albedo: Tuple[int, int, int]
    offset: np.ndarray
    source_object: Optional[LightSource]

    def __init__(self, albedo: Tuple[int, int, int], offset: List[np.float64]) -> None:
        self.albedo = albedo
        self.offset = np.array(offset, dtype=np.float64)
        self.source_object = None
    
    def get_intersection_params(self, ray: Ray):
        """
        Returns the possible intersection Parameters of the Object with a Ray
        """
        pass

    def get_normal(self, point: np.ndarray):
        """
        Returns the normal of the Object surface at a given point
        """
        pass

class Plane(Object):
    """
    Implementation for a plane
    """

    # Normal of plane is consistent
    normal: np.ndarray

    def __init__(self, vec1: List[np.float64], vec2: List[np.float64], offset: np.ndarray, 
        albedo: Tuple[int, int, int]) -> None:
        super().__init__(albedo, offset)

        # Compute the Normal form the two vectors inside the plane
        self.normal = normalise(np.array(np.cross(vec1, vec2), dtype=np.float64))

    def get_intersection_params(self, ray: Ray) -> List[np.float64]:
        ln = np.dot(ray.direction, self.normal)
        if np.abs(ln) < 1e-6:
            return [] # nearly parrallel -> no Intersect Point
        else:
            return [np.dot(self.offset - ray.offset, self.normal) / ln]
        
    def get_normal(self, point: np.ndarray):
        return self.normal

class Sphere(Object):
    """
    Implementation of a Object representing a Sphere
    """

    radius: np.float64
    
    def __init__(self, radius: np.float64, albedo: Tuple[int, int, int], offset: List[np.float64]) -> None:
        super().__init__(albedo, offset)
        self.radius = radius

    def get_intersection_params(self, ray: Ray):

        # Formula: See Documentation
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
    """
    Implementation of a Sphere, with a Light Source (Point Light)
    """

    def __init__(self, radius: np.float64, albedo: Tuple[int, int, int], offset: List[np.float64], intensity: int) -> None:
        super().__init__(radius, albedo, offset)
        self.source_object = PointLight(albedo, offset, intensity)

class CuboidVertical(Object):
    """
    Represents a cuboid (a box), with it's height always in the y-direction and thats rotated along the y-Axis
    """
    width_half: float
    height_half: float
    depth_half: float
    # Bounding Sphere (see Documentation)
    bounding_sphere: Sphere
    # Surface Planes
    x_y_surfaces: List[Plane]
    x_z_surfaces: List[Plane]
    y_z_surfaces: List[Plane]
    # Rotation Matrix
    rotation_matrix: np.ndarray
    rotation_matrix_inverse: np.ndarray

    def __init__(self, rotation: float, width:float, height: float, depth: float, albedo: Tuple[int, int, int], offset_center: List[np.float64]) -> None:
        super().__init__(albedo, offset_center)
        """
        Rotation is given in degrees
        """
        self.height_half = height / 2
        self.width_half = width / 2
        self.depth_half = depth / 2
        radius = np.linalg.norm([self.width_half, self.height_half, self.depth_half])
        self.bounding_sphere = Sphere(radius, BLACK, offset_center)
        self.x_y_surfaces = list([
            Plane([width, 0, 0], [0, height, 0], np.add(offset_center, [0,0, -self.depth_half]), BLACK),
            Plane([width, 0, 0], [0, height, 0], np.add(offset_center, [0,0, self.depth_half]), BLACK)
        ])
        self.x_z_surfaces = list([
            Plane([width, 0, 0], [0, 0, depth], np.add(offset_center, [0, -self.height_half, 0]), BLACK),
            Plane([width, 0, 0], [0, 0, depth], np.add(offset_center, [0, self.height_half, 0]), BLACK)
        ])
        self.y_z_surfaces = list([
            Plane([0, height, 0], [0, 0, depth], np.add(offset_center, [-self.width_half, 0, 0]), BLACK),
            Plane([0, height, 0], [0, 0, depth], np.add(offset_center, [self.width_half, 0, 0]), BLACK)
        ])
        # rotation must be convertet from degrees to radiants
        rot_rad = np.deg2rad(rotation)
        self.rotation_matrix = np.array([
            [np.cos(rot_rad), 0, -np.sin(rot_rad)],
            [0, 1, 0],
            [np.sin(rot_rad), 0, np.cos(rot_rad)]
        ])
        self.rotation_matrix_inverse = np.array([
            [np.cos(-rot_rad), 0, -np.sin(-rot_rad)],
            [0, 1, 0],
            [np.sin(-rot_rad), 0, np.cos(-rot_rad)]
        ])

    def get_intersection_params(self, ray: Ray):
        nearest_param: np.float64 = inf

        # transform the given ray into the Box Space, rotate it and bring it back into World Space to 
        # compute hitpoint with the planes (this means that no new implementation is neccessary since planes are 
        # already implemented)
        relative_offset_transformed = np.dot(self.rotation_matrix, (ray.offset - self.offset))
        new_offset = relative_offset_transformed + self.offset
        new_direction =  np.dot(self.rotation_matrix, ray.direction)
        ray_transformed = Ray(new_offset, new_direction)

        # Bounding Sphere Check
        if len(self.bounding_sphere.get_intersection_params(ray_transformed)) > 0:
            # Test all side planes and get the Parameters
            for plane in self.x_y_surfaces:
                params = plane.get_intersection_params(ray_transformed)
                # Plane is hit -> check whether the hitpoint is inside the boundaries of the Box
                if len(params) > 0 and params[0] < nearest_param:
                    x, y, z = ray_transformed.offset + params[0] * ray_transformed.direction - self.offset # Compute Intersect Point and bring it into the cubicle coordinate system
                    if x <= self.width_half and x >= -self.width_half and y <= self.height_half and y >= -self.height_half:
                        nearest_param = params[0]
            for plane in self.x_z_surfaces:
                params = plane.get_intersection_params(ray_transformed)
                # Plane is hit -> check whether the hitpoint is inside the boundaries of the Box
                if len(params) > 0 and params[0] < nearest_param:
                    x, y, z = ray_transformed.offset + params[0] * ray_transformed.direction - self.offset
                    if x <= self.width_half and x >= -self.width_half and z <= self.depth_half and z >= -self.depth_half:
                        nearest_param = params[0]
            for plane in self.y_z_surfaces:
                params = plane.get_intersection_params(ray_transformed)
                # Plane is hit -> check whether the hitpoint is inside the boundaries of the Box
                if len(params) > 0 and params[0] < nearest_param:
                    x, y, z = ray_transformed.offset + params[0] * ray_transformed.direction - self.offset
                    if y <= self.height_half and y >= -self.height_half and z <= self.depth_half and z >= -self.depth_half:
                        nearest_param = params[0]
            
            if nearest_param == inf:
                return [] # No hit
            return [nearest_param] # hit
        return [] # No hit
    
    def get_normal(self, point: np.ndarray):
        
        # determine on which side the given point is and return the normal (transformed back into World Space
        # using the matrix)

        # the tolerance of 1e-6 (+-) is used to combat inaccuracies of the computer
        x, y, z = np.dot(self.rotation_matrix_inverse, (point - self.offset))
        if x >= (-self.width_half - 1e-6) and x <= (-self.width_half + 1e-6):
            return np.dot(self.rotation_matrix_inverse, [-1, 0, 0])
        if x >= (self.width_half - 1e-6) and x <= (self.width_half + 1e-6):
            return np.dot(self.rotation_matrix_inverse, [1, 0, 0])
        if y >= (-self.height_half - 1e-6) and y <= (-self.height_half + 1e-6):
            return np.dot(self.rotation_matrix_inverse, [0, -1, 0])
        if y >= (self.height_half - 1e-6) and y <= (self.height_half + 1e-6):
            return np.dot(self.rotation_matrix_inverse, [0, 1, 0])
        if z >= (-self.depth_half - 1e-6) and z <= (-self.depth_half + 1e-6):
            return np.dot(self.rotation_matrix_inverse, [0, 0, -1])
        if z >= (self.depth_half - 1e-6) and z <= (self.depth_half + 1e-6):
            return np.dot(self.rotation_matrix_inverse, [0, 0, 1])
            