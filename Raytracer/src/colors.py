import numpy as np 
from typing import List


class RGBI:
    vals: np.ndarray
    illumination: int # whether the Object illuminates (in %)

    def __init__(self, vals: List[int], illumination: int = 0) -> None:
        self.vals = np.array(vals, dtype=np.uint16)
        self.illumination = illumination % 101

    def interpolate(self, b: 'RGBI') -> 'RGBI':
        vals = list(map(lambda x, y: np.clip(((x+y)/2), 0, 255), self.vals, b.vals))
        illu = np.clip(self.illumination + b.illumination, 0, 100) 
        return RGBI(vals, illu)

    def travel(self, degradation: float, distance: float) -> 'RGBI':
        return RGBI(self.vals, self.illumination - (degradation * distance))

    def get_val_array(self) -> np.ndarray:
        fac = np.divide(self.illumination, 100)
        return np.array(np.multiply(self.vals, fac), dtype=np.uint8)