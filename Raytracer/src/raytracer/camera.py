from typing import Iterable
import numpy as np
from raytracer.coordinate_utils import ZERO

from raytracer.coordinate_utils import Ray

class SimpleCamera():
    """
    Represents a Camera with Offset = [0, 0, 0] and the center of it's screen at [0, 0, -1] 
    Used to generate the primary rays
    """
    width: np.int16
    height: np.int16
    fov: np.float16
    tan_fov_half: np.float64
    aspect_ratio: np.float64

    def __init__(self, width: np.int16, height: np.int16, fov: np.float16) -> None:
        [self.width, self.height, self.fov] = [width, height, fov]
        self.tan_fov_half = np.tan(np.deg2rad(np.divide(fov, 2)))
        self.aspect_ratio = np.divide(width, height)
    
    def get_primary_rays(self) -> Iterable[Ray]:
        """
        Creates all primary rays and returns them, so that for-each can be used to iterate over them
        """
        for y in range(0, self.height):
            # Formulas: See Documentation
            pixel_screen_y: np.float64 = (y+0.5) / self.height
            pixel_cam_y = (1 - 2*pixel_screen_y) * self.tan_fov_half 
            for x in range(0, self.width):
                pixel_screen_x: np.float64 = (x+0.5) / self.width
                pixel_cam_x = (2*pixel_screen_x - 1) * self.aspect_ratio * self.tan_fov_half 
                yield(Ray(ZERO, [pixel_cam_x, pixel_cam_y, -1]))

    def set_resolution(self, width: np.int16, height: np.int16) -> None:
        """
        Changes the resolution
        """
        [self.width, self.height] = [width, height]