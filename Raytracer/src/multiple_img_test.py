from time import time_ns, struct_time 

from PIL import Image
from camera import CameraSimple
from objects import Object, Sphere
from colors import RGBI
from coordinates import *
from trace_algorithm import Scenery
from pathlib import Path
from math import floor

IMG_FOLDER = Path(__file__).resolve().parent.joinpath('imgs')


OBJECTS = [
    Sphere(RGBI([0,0,255],0), 4, np.array([0, 0, -20])),
    Sphere(RGBI([255,0,0],0), 9, np.array([20, 0, -35])),
    Sphere(RGBI([0,255,255],0), 13, np.array([-5, 15, -40]))
]

SOURCE = Sphere(RGBI([255,255,255], 100), 0.1, np.array([0, 10, -10]))

FOV = 90

def post_render_stuff(ts: float, te: float, data: np.ndarray, img_name: str):
    dt = te-ts
    [h, m, s, ms] = [floor(dt/(1e9*3600)), floor(dt/(1e9*60))%60, floor(dt/1e9)%60, floor(dt/1e6)%1e3]
    print(f"Rendering took: {h}:{m}:{s}:{ms} (h:m:s:ms)\n")
    img = Image.fromarray(data)
    img.save(IMG_FOLDER.joinpath(img_name))

def small_image():
    print("----------------\nsmall image with few revisions")
    camera = CameraSimple(width=480, height=360, fov=90)
    scenery = Scenery(OBJECTS, camera ,SOURCE, revisions=2, degradation=5)
    start_time = time_ns()
    data =  scenery.render_img_to_array()
    post_render_stuff(start_time, time_ns(), data, 'small.png')
    
    
def medium_image():
    print("----------------\nmedium (HD) image with few revisions")
    camera = CameraSimple(width=1920, height=1080, fov=90)
    scenery = Scenery(OBJECTS, camera ,SOURCE, revisions=2, degradation=1)
    start_time = time_ns()
    data = scenery.render_img_to_array()
    post_render_stuff(start_time, time_ns(), data, 'medium.png')

def large_image():
    print("----------------\n4k image with few revisions")
    camera = CameraSimple(width=3840, height=2160, fov=90)
    scenery = Scenery(OBJECTS, camera ,SOURCE, revisions=2, degradation=1)
    start_time = time_ns()
    data = scenery.render_img_to_array()
    post_render_stuff(start_time, time_ns(), data, 'large.png')

if __name__ == '__main__':
    small_image()
    medium_image()
    large_image()