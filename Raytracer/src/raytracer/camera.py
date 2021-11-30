from typing import Iterable
import numpy as np
from raytracer.coordinate_utils import ZERO

from raytracer.coordinate_utils import Ray

"TODO: Tests"
class SimpleCamera():
    width: np.int16
    height: np.int16
    fov: np.float16
    tan_fov_half: np.float64
    aspect_ratio: np.float64

    def __init__(self, width: np.int16, height: np.int16, fov: np.float16) -> None:
        [self.width, self.height, self.fov] = [width, height, fov]
        self.tan_fov_half = np.tan(np.deg2rad(np.divide(fov, 2)))
        self.aspect_ratio = np.divide(width, height)
    
    def get_primary_rays(self) -> Iterable[Ray]: #Correct Return Type ?
        """
        usage: for ray in camera.get_primary_rays(): ...
        """
        for y in range(0, self.height):
            pixel_screen_y: np.float64 = np.divide(y+0.5, self.height)
            pixel_cam_y = (1 - 2*pixel_screen_y) * self.tan_fov_half #np.multiply(np.subtract(1, np.multiply(2, pixel_screen_y)), self.tan_fov_half)
            for x in range(0, self.width):
                pixel_screen_x: np.float64 = np.divide(x+0.5, self.width)
                pixel_cam_x = (2*pixel_screen_x - 1) * self.aspect_ratio * self.tan_fov_half #np.multiply(np.multiply(np.subtract(np.multiply(2, pixel_screen_x), 1), self.aspect_ratio), self.tan_fov_half)
                yield(Ray(ZERO, [pixel_cam_x, pixel_cam_y, -1]))

    def set_resolution(self, width: np.int16, height: np.int16) -> None:
        [self.width, self.height] = [width, height]