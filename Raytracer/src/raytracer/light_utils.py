import numpy as np
from typing import List, Tuple


def get_diffuse_surface_color(albedo: np.ndarray, l_i: 'Light', normal: np.ndarray, light_direction: np.ndarray) -> 'Light':
    """
    Simulates the Light hitting a surface at a given angle (See documentation for formula)
    :param albedo: Albedo of the surface
    :param l_i: Incoming Light
    :param normal: Normal of the surface
    :param light_direction: Direction of the Light (Points away from the surface)
    """
    
    # Factor depending on the angle (set to at least 0.4, otherwise areas where the rays hit nearly parrallel 
    # would be to dark)
    fac = max([0.4, np.dot(normal, light_direction)])

    rgb = (np.array(albedo) / np.pi) * np.array(l_i.rgb) * fac
    intensity = l_i.intensity * fac
    return Light(
        rgb=rgb,
        intensity=intensity
    )

class Light:
    """
    Light information consisting of rgb-color and intensity
    """

    rgb: Tuple[int, int, int]
    intensity: int

    def __init__(self, rgb: Tuple[int, int, int], intensity) -> None:
        self.rgb = rgb
        self.intensity = intensity

    def travel(self, distance: float) -> 'Light':
        """
        Simulates the Light travelling over a distance using the degredation formula of a Point Light
        """
        new_intensity = self.intensity / (4 * np.pi * distance**2)
        return Light(
            rgb=self.rgb,
            intensity=new_intensity
        )
    
    def resolve(self) -> np.ndarray:
        """
        Resolves the Information into a array of RGB-Values (between 0 and 255)
        """
        inten = self.intensity / 100
        return np.clip(np.array(
            [self.rgb[0] * inten,
            self.rgb[1] * inten,
            self.rgb[2] * inten]
        ), 0, 255)


"""
Some useful Colors
"""
BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255,255,255)
