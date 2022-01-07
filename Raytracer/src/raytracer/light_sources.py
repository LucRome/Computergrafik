import numpy as np
from typing import List, Optional, Tuple

from .light_utils import Light

"""
Classes and Interfaces to handle Light Sources
"""

class LightSource:
    """
    Generic Interface of a Light Source
    """
    light_intensity: float
    color: Tuple[int, int, int]
    offset: np.ndarray

    def __init__(self, light_intensity: int, color: Tuple[int, int, int], offset: np.ndarray) -> None:
        self.light_intensity = light_intensity
        self.color = color
        self.offset = offset

    def get_light_intensity(self, point: np.ndarray) -> Light:
        """
        Returns the Light intensity at a given Point
        """
        pass

class PointLight(LightSource):
    """
    Implementation of a Light Source representing a point Light
    """

    def __init__(self, color: Tuple[int, int, int], offset: np.ndarray, light_intensity: int) -> None:
        super().__init__(light_intensity, color, offset)

    def get_light_intensity(self, point: np.ndarray) -> Light:
        """
        Returns the Light intensity at a given Point using the Light degradation of a Point Light
        (See Documentation for formula)
        """
        radius = np.linalg.norm(np.subtract(point, self.offset))
        new_intensity = self.light_intensity / (4 * np.pi * radius**2)
        return Light(
            self.color,
            new_intensity
        )
    
        