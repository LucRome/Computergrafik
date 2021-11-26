from math import inf
from colors import RGBI
from camera import CameraSimple
from coordinates import *
from objects import Object
from typing import List
from PIL import Image

import numpy as np

class Scenery:
    objects: List[Object]
    camera: CameraSimple
    source: Object
    max_revisions: int
    degradation: int
    
    def __init__(self, objects: List[Object], camera: CameraSimple, source: Object, revisions: int, degradation: float) -> None:
        self.objects = list(objects)
        self.camera = camera
        self.source = source
        self.objects.append(source)
        self.max_revisions = revisions
        self.degradation = degradation

    def render_img_to_array(self) -> np.ndarray:
        pixels_msg = np.divide(np.multiply(self.camera.width, self.camera.height), 100)
        data = np.zeros((self.camera.height, self.camera.width, 3), dtype=np.uint8)

        n = 0
        percent = 0
        for x in range(0,self.camera.width):
            for y in range(0,self.camera.height):
                rgbi = self.send_ray(x/self.camera.width, y/self.camera.height)
                data[y, x] = rgbi.get_val_array()
                n = (n+1)%pixels_msg
                if n == 0:
                    print(f"Rendering:\t{percent}%\tcompleted")
                    percent += 1

        return data

    
    def send_ray(self, x: int, y: int) -> RGBI:
        ray = self.camera.get_ray(x,y)
        return self.trace_ray(ray)

    def trace_ray(self, ray: Ray, rev: int = 0) -> RGBI:
        normalise(ray.direction)
        if rev > self.max_revisions:
            return RGBI([0,0,0]) # Shadow Ray
        else:
            # get intersect point
            smallest_param: float = inf
            nearest_object: Object = None
            for object in self.objects:
                intersect_point_params = object.get_intersect_pnt_params(ray)
                for param in intersect_point_params:
                    if param > 0 and param < smallest_param:
                        smallest_param = param
                        nearest_object = object
            
            if nearest_object is None:
                return RGBI([0,0,0], 0) # Background

            intersect_point = np.add(ray.offset, np.multiply(ray.direction, smallest_param))
            distance = np.linalg.norm(np.subtract(ray.offset, intersect_point))

            if nearest_object == self.source:
                return nearest_object.rgb.travel(self.degradation, distance)

            source_ray = self.get_ray_to_source(intersect_point)
            if (self.source_ray_visible(
                dir_in=ray.direction,
                dir_out=source_ray.direction,
                normal=nearest_object.get_normal(intersect_point)
            )):
                if (nearest_object.is_source):
                    return nearest_object.rgb.travel(self.degradation, distance) # 
                else:
                    rgb_source = self.trace_ray(source_ray, rev + 1)
                    return rgb_source.interpolate(nearest_object.rgb).travel(self.degradation, distance)
            else:
                return RGBI(nearest_object.rgb.vals, 0) # Shadow

            
    def get_ray_to_source(self, point: np.ndarray) -> Ray:
        dir = np.subtract(self.source.offset, point)
        normalise(dir)
        return Ray(point, dir)
    
    def source_ray_visible(self, dir_in: np.ndarray, dir_out: np.ndarray, normal: np.ndarray):
        alpha_1 = np.rad2deg(angle(np.multiply(dir_in, -1) ,normal)) # needed so that in and out vector show are in the same direction
        alpha_2 = np.rad2deg(angle(dir_out, normal))

        if (alpha_1 < 90) == (alpha_2 < 90):
            return True
        else:
            return False
