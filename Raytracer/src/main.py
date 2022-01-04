from raytracer.trace_algorithm import Scenery
from raytracer.utils import save_as_img_timed
from raytracer.camera import SimpleCamera
from raytracer.coordinate_utils import ZERO
from raytracer.objects import LightSphere, Sphere, Plane, CuboidVertical
from raytracer.light_utils import *

from utils import test_single_pixel

from pathlib import Path

IMG_PATH = Path(__file__).resolve().parent.joinpath('imgs')

if not IMG_PATH.exists():
    IMG_PATH.mkdir()

OBJECTS = [
    # CuboidVertical(
    #     rotation=45,
    #     width=4,
    #     height=6,
    #     depth=4,
    #     albedo=RED,
    #     offset_center=[0, -4, -10]
    # ),
    LightSphere(
        radius=0.5,
        albedo=WHITE,
        offset=[-2,0,-5],
        intensity=10000000
    ),
    Sphere(2.0, RED, [0,5,-13]),
    #Sphere(4.0, BLUE, [3,2,-12]),
    Plane(vec1=[1,0,0], vec2=[0,1,0], offset=[0,0,-20], albedo=(120,120,120)),
]

FOV = 60
MAX_DEPTH = 3
LIGHT_DEGRADATION = 2

"""
Small Image
"""
camera = SimpleCamera(480,360,FOV)
scenery = Scenery(OBJECTS, camera, MAX_DEPTH, LIGHT_DEGRADATION)

test_single_pixel(scenery, pixel_x=227, pixel_y=73)
save_as_img_timed(IMG_PATH.joinpath('small.png'), scenery)

"""
Medium Image
"""
camera.set_resolution(1920, 1080)
save_as_img_timed(IMG_PATH.joinpath('medium.png'), scenery)