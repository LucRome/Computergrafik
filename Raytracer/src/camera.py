import numpy as np
from coordinates import Ray

# Would use a c2w matrix but no idea how it works atm
"""
class Camera:
    c2w_matrix: List[Vect] # Column major
    width: int # Resolution.x
    height: int # Resolution.y
    fov: int
    w_prime: Vect

    def __init__(self, c2w_matrix: List[Vect], width: int, height: int, fov: int) -> None:
        [self.c2w_matrix, self.width, self.height, self.fov] = [c2w_matrix, int(width), int(height), int(fov)]
        a = add_vec(
            c2w_matrix[0].times_factor(-width/2), 
            c2w_matrix[1].times_factor(height/2)
        )
        self.w_prime = sub_vec(
            a,
            c2w_matrix[2].times_factor(height/(2*tan(fov*0.5)))
        )
    
    def get_ray(self, x: int, y:int) -> Ray:
        a = add_vec(
            self.c2w_matrix[0].times_factor(x),
            self.c2w_matrix[1].times_factor(-y) # commutative???
        )
        direc = add_vec(a, self.w_prime)
        direc.normalise()
        
        # Annahme: c2w_matrix[3] is the offset
        return Ray(self.c2w_matrix[3], direc)
"""

class CameraSimple:
    width: np.int32
    height: np.int32
    fov: np.int32
    aspect_ratio: np.float32
    tan_alpha_half: np.float32
    def __init__(self, width: np.int32, height: np.int32, fov: np.int32) -> None:
        self.width = np.int32(width)
        self.height = np.int32(height)
        self.fov = np.int32(fov)
        self.aspect_ratio = np.divide(self.width, self.height)
        self.tan_alpha_half = np.tan(fov/2)

    def get_ray(self, x: int, y: int) -> Ray:
        x_cam = (2 * x - 1) * self.aspect_ratio * self.tan_alpha_half
        y_cam = (1 - 2 * y) * self.tan_alpha_half
        return Ray(offset=np.array([0,0,0]), direction=np.array([x_cam, y_cam, -1], dtype=np.float32))