import numpy as np

"""
Utils for Coordinates
Coordinates: [x,y,z] (Datatype: float)
"""
def normalise(vec: np.ndarray) -> None:
    nrm = np.linalg.norm(vec)
    for i in range(0, len(vec)):
        vec[i] = np.divide(vec[i], nrm)

def angle(a: np.ndarray, b: np.ndarray) -> np.float32:
    normalise(a)
    normalise(b)
    return np.arccos(np.clip(np.dot(a, b), -1.0, 1.0))

def rad2deg(angle: float) -> np.float32:
    "radial to degrees"
    return np.rad2deg(angle)


class Ray:
    offset: np.ndarray
    direction: np.ndarray

    def __init__(self, offset: np.ndarray, direction: np.ndarray) -> None:
        self.offset = offset
        self.direction = direction