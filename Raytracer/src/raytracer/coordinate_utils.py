import numpy as np

"""
Functions and classes to improve the handling of Coordinates
"""

class Ray():
    """
    Parametric Representation of a ray
    Has offset vector and (normalised) direction vector
    """
    offset: np.ndarray
    direction: np.ndarray
    
    def __init__(self, offset: np.ndarray, direction: np.ndarray) -> None:
        self.offset = offset
        self.direction = normalise(direction)


def normalise(vec: np.ndarray) -> np.ndarray:
    """
    Normalises the given vector
    """
    norm = np.linalg.norm(vec)
    return vec / norm

def is_normalised(vec: np.ndarray) -> bool:
    """
    True if |vec| == 1
    """
    return (np.linalg.norm(vec) == 1)

"""
Useful Coordinates and Vectors
"""

ZERO = np.array([0,0,0], dtype=np.float64)
CAMERA_SCREEN_MIDDLE = np.array([0,0,-1], dtype=np.float64)
CAMERA_SCREEN_DIR1 = np.array([1,0,0], dtype=np.float64)
CAMERA_SCREEN_DIR2 = np.array([0,1,0], dtype=np.float64)