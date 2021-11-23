from math import sqrt
from typing import List

import numpy as np

from colors import RGBI


from coordinates import Vect, Ray

class Object:
    rgb: RGBI
    is_source: bool
    offset: Vect

    def __init__(self, rgbi, is_source, offset) -> None:
        self.rgb = rgbi
        self.is_source = is_source
        self.offset = offset

    def get_intersect_pnt_params(self, ray: Ray) -> List[float]:
        pass

    def get_normal(self, point: Vect) -> Vect:
        pass

class Sphere(Object):
    radius: float
    offset: Vect

    def __init__(self, rgbi: RGBI, radius: float, offset: Vect) -> None:
        is_source = rgbi.illumination > 0
        super().__init__(rgbi, is_source, offset)
        self.radius = radius

    
    def get_intersect_pnt_params(self, ray: Ray) -> np.ndarray: #returns t_0 and t_1
        a = ray.direction.square()
        b = 2 * ray.direction.dot(ray.offset.sub(self.offset))
        c = self.offset.sub(ray.offset).sum() ** 2 - self.radius**2

        discriminant = b**2 - 4*a*c
        if discriminant < 0:
            return np.array([])
        elif discriminant == 0:
            return np.array([-b/(2*a)])
        else:
            q = - np.divide((b + sign(b) * np.sqrt(b**2 - 4*a*c)), 2)
            return np.array([np.divide(q,a), np.divide(c,a)])
        
    def get_normal(self, point: Vect) -> Vect:
        vec = point.sub(self.offset)
        vec.normalise()
        return vec

def sign(x: float):
    return -1 if x < 0 else 1