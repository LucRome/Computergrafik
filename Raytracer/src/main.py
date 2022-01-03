from utils import save_rgb_array_to_file
from raytracer.trace_algorithm import Scenery
from raytracer.utils import save_as_img_timed
from raytracer.camera import SimpleCamera
from raytracer.coordinate_utils import ZERO
from raytracer.materials import WHITE_LIGHTSOURCE, RED, BLUE, GREEN, Material
from raytracer.objects import LightSphere, Sphere, Plane, CuboidVertical

from utils import test_single_pixel

from pathlib import Path

IMG_PATH = Path(__file__).resolve().parent.joinpath('imgs')

if not IMG_PATH.exists():
    IMG_PATH.mkdir()

OBJECTS = [
    CuboidVertical(45, 4, 6, 4, BLUE, [0, 0, -10]),
    LightSphere(1, [255,255,255], [0,5,-5]),
    Sphere(2.0, RED, [0,0,-10]),
    Sphere(4.0, BLUE, [3,2,-12]),
    Plane(vec1=[1,0,0], vec2=[0,1,0], offset=[0,0,-20], material=Material([120,120,120], 0)),
]

FOV = 60
MAX_DEPTH = 3
LIGHT_DEGRADATION = 2

"""
Small Image
"""
camera = SimpleCamera(480,360,FOV)
scenery = Scenery(OBJECTS, camera, MAX_DEPTH, LIGHT_DEGRADATION)

test_single_pixel(scenery, pixel_x=205, pixel_y=320)
save_as_img_timed(IMG_PATH.joinpath('small.png'), scenery)

"""
Medium Image
"""
camera.set_resolution(1920, 1080)
save_as_img_timed(IMG_PATH.joinpath('medium.png'), scenery)