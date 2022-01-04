import numpy as np
from typing import List, Optional, Tuple

from .light_utils import Light

class LightSource:
    light_intensity: float
    color: Tuple[int, int, int]
    offset: np.ndarray

    def __init__(self, light_intensity: int, color: Tuple[int, int, int], offset: np.ndarray) -> None:
        self.light_intensity = light_intensity
        self.color = color
        self.offset = offset

    def get_light_intensity(self, point: np.ndarray) -> Light:
        pass

class PointLight(LightSource):

    def __init__(self, color: Tuple[int, int, int], offset: np.ndarray, light_intensity: int) -> None:
        super().__init__(light_intensity, color, offset)

    def get_light_intensity(self, point: np.ndarray) -> Light:
        radius = np.linalg.norm(np.subtract(point, self.offset))
        new_intensity = self.light_intensity / (4 * np.pi * radius**2)
        return Light(
            self.color,
            new_intensity
        )
    
        