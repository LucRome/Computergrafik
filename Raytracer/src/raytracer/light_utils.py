import numpy as np
from typing import List, Tuple


def get_diffuse_surface_color(albedo: np.ndarray, l_i: 'Light', normal: np.ndarray, light_direction: np.ndarray) -> 'Light':
    rgb = (np.array(albedo) / np.pi) * np.array(l_i.rgb) * max([0, np.dot(normal, light_direction)])
    return Light(
        rgb=rgb,
        intensity=l_i.intensity
    )

class Light:
    rgb: Tuple[int, int, int]
    intensity: int

    def __init__(self, rgb: Tuple[int, int, int], intensity) -> None:
        self.rgb = rgb
        self.intensity = intensity

    def travel(self, distance: float) -> 'Light':
        new_intensity = self.intensity / (4 * np.pi * distance**2)
        return Light(
            rgb=self.rgb,
            intensity=new_intensity
        )
    
    def resolve(self) -> np.ndarray:
        inten = self.intensity / 100
        return np.clip(np.array(
            [self.rgb[0] * inten,
            self.rgb[1] * inten,
            self.rgb[2] * inten]
        ), 0, 255)

BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255,255,255)
