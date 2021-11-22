from typing import List
from math import sqrt, acos, pi

"""
Utils for Coordinates
Coordinates: [x,y,z] (Datatype: float)
"""
class Vect:
    vals: List[float]
    def __init__(self, vals: List[float]):
        self.vals = list()
        for val in vals:
            self.vals.append(val)

    def sum(self) -> float:
        res = 0
        for i in range(0, len(self.vals)):
            res += self.vals[i]**2
        return sqrt(res)

    def normalise(self) -> None:
        s = self.sum()
        for i in range(0, len(self.vals)):
            self.vals[i] /= s

    def times_factor(self, fac: float) -> 'Vect':
        ret = list()
        for val in self.vals:
            ret.append(val * fac)
        return Vect(ret)

    def dot(self, b: 'Vect') -> float:
        res = 0
        for i in range(0, len(self.vals)):
            res += self.vals[i] * b.vals[i]
        return res

    def square(self) -> float:
        return self.dot(self)

def add_vec(a: Vect, b: Vect) -> Vect:
    lst = list()
    for i in range(0, len(a.vals)):
        lst.append(a.vals[i] + b.vals[i])
    return Vect(lst)
    
def sub_vec(a: Vect, b: Vect) -> Vect:
    lst = list()
    for i in range(0, len(a.vals)):
        lst.append(a.vals[i] - b.vals[i])
    return Vect(lst)

def angle_vec(a: Vect, b: Vect) -> float:
    "Winkel im Bogenmaß (also von 0 - 2pi)"
    a.normalise()
    b.normalise()
    dp = a.dot(b)
    if dp > 1:
        dp = 1
    elif dp < -1:
        dp = -1
    return acos(dp)

def bm_to_am(angle: float) -> float:
    "Bogenmaß zu Winkelmaß"
    return angle * 360 / (2*pi)

class Ray:
    offset: Vect
    direction: Vect

    def __init__(self, offset: Vect, direction: Vect) -> None:
        self.offset = offset
        self.direction = direction