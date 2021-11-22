from typing import List


class RGBI:
    vals: List[int]
    illumination: int # whether the Object illuminates (in %)

    def __init__(self, vals: List[int], illumination: int = 0) -> None:
        self.vals = vals
        self.illumination = illumination

    def interpolate(self, b: 'RGBI') -> 'RGBI':
        vals = list()
        for i in range(0,3):
            vals.append((self.vals[i] + b.vals[i]) / 2)
        illu = self.illumination + b.illumination
        return RGBI(vals, illu)

    def travel(self, degradation: int, distance: float) -> 'RGBI':
        return RGBI(self.vals, self.illumination - (degradation * distance))

    def to_array(self) -> List[int]:
        lst = list()
        for i in range(0,3):
            lst.append(self.vals[i] * self.illumination / 100)
        return lst