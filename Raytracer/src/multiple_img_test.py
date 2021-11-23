from time import time_ns, struct_time 

from PIL.Image import Image
from camera import CameraSimple
from objects import Object, Sphere
from colors import RGBI
from coordinates import *
from trace_algorithm import Scenery
from pathlib import Path
from math import floor

IMG_FOLDER = Path(__file__).resolve().parent.joinpath('imgs')


OBJECTS = [
    Sphere(RGBI([0,0,255],0), 4, Vect([0, 0, -20])),
    Sphere(RGBI([255,0,0],0), 9, Vect([20, 0, -35])),
    Sphere(RGBI([0,255,255],0), 13, Vect([-5, 15, -40]))
]

SOURCE = Sphere(RGBI([255,255,255], 100), 0.1, Vect([0, 10, -10]))

FOV = 90

def post_render_stuff(ts: float, te: float, img: Image, img_name: str):
    dt = te-ts
    [h, m, s, ms] = [floor(dt/(1e9*3600)), floor(dt/(1e9*60))%60, floor(dt/1e9)%60, floor(dt/1e6)%1e3]
    print(f"Rendering took: {h}:{m}:{s}:{ms} (h:m:s:ms)\n")
    img.save(IMG_FOLDER.joinpath(img_name))

def small_image():
    print("----------------\nsmall image with few revisions")
    camera = CameraSimple(width=480, height=360, fov=90)
    scenery = Scenery(OBJECTS, camera ,SOURCE, revisions=2, degradation=0)
    start_time = time_ns()
    img = scenery.render_img()
    post_render_stuff(start_time, time_ns(), img, 'small.png')
    
    
def medium_image():
    print("----------------\nmedium (HD) image with few revisions")
    camera = CameraSimple(width=1920, height=1080, fov=90)
    scenery = Scenery(OBJECTS, camera ,SOURCE, revisions=2, degradation=0)
    start_time = time_ns()
    img = scenery.render_img()
    post_render_stuff(start_time, time_ns(), img, 'medium.png')

def large_image():
    print("----------------\n4k image with few revisions")
    camera = CameraSimple(width=3840, height=2160, fov=90)
    scenery = Scenery(OBJECTS, camera ,SOURCE, revisions=2, degradation=0)
    start_time = time_ns()
    img = scenery.render_img()
    post_render_stuff(start_time, time_ns(), img, 'large.png')

if __name__ == '__main__':
    small_image()
    medium_image()
    large_image()