from typing import List
import numpy as np
from typing import List


"""
Definitions regarding the Material of Objects
"""

ILLUMINATION_MAX = 100
RGB_MAX = 256

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
    
    def travel(self, distance: np.uint32, degradation: np.float16) -> 'Material':
        """
        Params:
            distance: traveled distance (> 0)
            degradation: light degradation per 1 unit (> 0)
        """
        return Material(
            rgb=self.rgb,
            illumination=self.illumination - (degradation * distance)
        )