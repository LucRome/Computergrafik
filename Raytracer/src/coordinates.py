from typing import List
import numpy as np

"""
Utils for Coordinates
Coordinates: [x,y,z] (Datatype: float)
"""
class Vect:
    vals: np.ndarray
    def __init__(self, vals: List[float]):
        self.vals = np.array(vals, dtype=np.float32)

    def sum(self) -> np.float32:
        return np.linalg.norm(self.vals)

    def normalise(self) -> None:
        self.vals = self.vals / (np.linalg.norm(self.vals)) 

    def times_factor(self, fac: float) -> 'Vect':
        return Vect(np.multiply(self.vals, fac))

    def dot(self, b: 'Vect') -> np.float32:
        return np.dot(self.vals, b.vals)

    def square(self) -> np.float32:
        return np.dot(self.vals, self.vals)

    def add(self, b: 'Vect') -> 'Vect':
        return Vect(np.add(self.vals, b.vals))
    
    def sub(self, b: 'Vect') -> 'Vect':
        return Vect(np.subtract(self.vals, b.vals))
    
    def angle_to(self, b:'Vect') -> np.float32:
        "angle in radians"
        self.normalise()
        b.normalise()
        return np.arccos(np.clip(self.dot(b), -1.0, 1.0))

def rad2deg(angle: float) -> float:
    "Bogenmaß zu Winkelmaß"
    return np.rad2deg(angle)

class Ray:
    offset: Vect
    direction: Vect

    def __init__(self, offset: Vect, direction: Vect) -> None:
        self.offset = offset
        self.direction = direction