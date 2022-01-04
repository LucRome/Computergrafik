import numpy as np
from typing import List, Tuple


def get_diffuse_surface_color(albedo: np.ndarray, l_i: float, normal: np.ndarray, light_direction: np.ndarray) -> List[int]:
    vals = (np.array(albedo) / np.pi) * l_i * max([0, np.dot(normal, light_direction)])
    return np.clip(vals, 0, 255)


BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255,255,255)
