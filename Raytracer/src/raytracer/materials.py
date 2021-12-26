from typing import List
import numpy as np
from typing import List


"""
Definitions regarding the Material of Objects
"""

ILLUMINATION_MAX = 100
RGB_MAX = 256

" Rename Class (isn't the material of an Object, but the light information of a ray) "
class Material:
    rgb: np.ndarray
    illumination: np.uint8

    def __init__(self, rgb: List[np.uint8], illumination: np.uint8) -> None:
        """
        Params:
            rgb: [r, g, b] (0 < x < 256)
            illumination: scalar 0 < x < 100
        """
        self.rgb = np.array(np.clip(rgb, 0, 255), dtype=np.uint16)
        self.illumination = np.clip(illumination, 0, ILLUMINATION_MAX)

    def interpolate(self, b: 'Material') -> 'Material':
        return Material(
            rgb=list(map(lambda x,y: (x+y)/2, self.rgb, b.rgb)),
            illumination=np.clip(self.illumination + b.illumination, 0, ILLUMINATION_MAX) 
        )
    
    def travel(self, distance: np.float64, degradation: np.float16) -> 'Material':
        """
        Params:
            distance: traveled distance (> 0)
            degradation: light degradation per 1 unit (> 0)
        """
        return Material(
            rgb=self.rgb,
            illumination=self.illumination - (degradation * distance)
        )
    
    def to_rgb_array(self) -> np.ndarray:
        fac = self.illumination / 100
        tmp = list(map(lambda x: np.clip(x * fac, 0, 255), self.rgb))
        return np.array(tmp, dtype=np.uint8)

"""
Useful Colours
"""
SHADOW_MATERIAL = Material([0,0,0],0)
RED = Material([255, 0, 0],0)
GREEN = Material([0,255,0],0)
BLUE = Material([0,0,255],0)

WHITE = Material([255,255,255],0)
WHITE_LIGHTSOURCE = Material([255,255,255],100)