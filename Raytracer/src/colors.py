import numpy as np 
from typing import List


class RGBI:
    vals: np.ndarray
    illumination: int # whether the Object illuminates (in %)

    def __init__(self, vals: List[int], illumination: int = 0) -> None:
        self.vals = np.array(vals, dtype=np.int8)
        self.illumination = illumination % 101

    def interpolate(self, b: 'RGBI') -> 'RGBI':
        vals = np.array(list(map(lambda x, y: (x+y)/2, self.vals, b.vals)))
        illu = (self.illumination + b.illumination) % 101
        return RGBI(vals, illu)

    def travel(self, degradation: int, distance: float) -> 'RGBI':
        return RGBI(self.vals, self.illumination - (degradation * distance))

    def get_val_array(self) -> np.ndarray:
        return self.vals