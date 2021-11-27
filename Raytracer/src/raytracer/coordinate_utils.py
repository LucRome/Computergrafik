import numpy as np

class Ray():
    offset: np.ndarray
    direction: np.ndarray
    
    def __init__(self, offset: np.ndarray, direction: np.ndarray) -> None:
        self.offset = offset
        self.direction = normalise(direction)


def normalise(vec: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vec)
    return vec/norm # the same as np.divide(vec, norm)

def is_normalised(vec: np.ndarray) -> bool:
    return (np.linalg.norm(vec) == 1)