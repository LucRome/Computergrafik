from coordinates import *
from camera import *
from colors import *
from objects import *
from trace_algorithm import *

from PIL import Image
import numpy as np

H = 500
W = 500
REVISIONS = 2

objects = [
    Sphere(RGBI([0,255,0], 0), 1, Vect([0,0,-4])), # green sphere (no source)
]

source = Sphere(RGBI([255,255,255], 100), 0.1, Vect([0, 5, -1])) # white source

camera = CameraSimple(W, H, 70)

scenery = Scenery(objects, camera, source, REVISIONS)

data = np.zeros((H, W, 3), dtype=np.uint8)

for x in range(0,W):
    for y in range(0,H):
        rgbi = scenery.send_ray(x/W,y/W)
        data[y, x] = rgbi.to_array()

img = Image.fromarray(data, 'RGB')
img.save('my.png')
img.show()