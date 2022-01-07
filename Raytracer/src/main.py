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
    # Planes on the sides
    Plane(vec1=[1,0,0], vec2=[0,0,-1], offset=[0,20,0], albedo=WHITE),
    Plane(vec1=[1,0,0], vec2=[0,0,-1], offset=[0,-20,0], albedo=WHITE),
    Plane(vec1=[1,0,0], vec2=[0,1,0], offset=[0,0,-200], albedo=WHITE),
    Plane(vec1=[0,1,0], vec2=[0,0,1], offset=[25,0,0], albedo=(82, 147, 250)),
    Plane(vec1=[0,1,0], vec2=[0,0,1], offset=[-25,0,0], albedo=RED),
    # Vertical Cuboids
    CuboidVertical(rotation=45, width=12.5, height=40, depth=12.5,
        albedo=(180, 180, 180), offset_center=[10, -10, -160]),
    CuboidVertical(rotation=0, width=12.5, height=30, depth=12.5,
        albedo=(250, 250, 82), offset_center=[-10, -20, -160]),
    #Light
    LightSphere(radius=2.5, albedo=WHITE, offset=[0, 19.2, -150], intensity=10000000000),
]

FOV = 20

"""
Small Image
"""
camera = SimpleCamera(480,360,FOV)
scenery = Scenery(OBJECTS, camera)

test_single_pixel(scenery, pixel_x=227, pixel_y=73)
save_as_img_timed(IMG_PATH.joinpath('small.png'), scenery)

"""
Medium Image
"""
camera.set_resolution(1920, 1080)
save_as_img_timed(IMG_PATH.joinpath('medium.png'), scenery)