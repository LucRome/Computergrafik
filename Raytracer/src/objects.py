from math import sqrt
from typing import List
from colors import RGBI


from coordinates import Vect, Ray, add_vec, sub_vec

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

    
    def get_intersect_pnt_params(self, ray: Ray) -> List[float]: #returns t_0 and t_1
        a = ray.direction.square()
        b = 2 * ray.direction.dot(sub_vec(ray.offset, self.offset))
        c = sub_vec(self.offset, ray.offset).sum() ** 2 - self.radius**2

        discriminant = b**2 - 4*a*c
        if discriminant < 0:
            return list()
        elif discriminant == 0:
            return list([-b/(2*a)])
        else:
            q = - 0.5 * (b + sign(b) * sqrt(b**2 - 4*a*c))
            return list([q/a, c/q])
        
    def get_normal(self, point: Vect) -> Vect:
        vec = sub_vec(point, self.offset)
        vec.normalise()
        return vec

def sign(x: float):
    return -1 if x < 0 else 1