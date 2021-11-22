from math import inf
from colors import RGBI
from camera import CameraSimple
from coordinates import *
from objects import Object
from typing import List

DEGRADATION = 0

class Scenery:
    objects: List[Object]
    camera: CameraSimple
    source: Object
    max_revisions: int
    
    def __init__(self, objects: List[Object], camera: CameraSimple, source: Object, revisions: int) -> None:
        self.objects = list(objects)
        self.camera = camera
        self.source = source
        self.objects.append(source)
        self.max_revisions = revisions
    
    def send_ray(self, x: int, y: int) -> RGBI:
        ray = self.camera.get_ray(x,y)
        return self.trace_ray(ray)

    def trace_ray(self, ray: Ray, rev: int = 0) -> RGBI:
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

            intersect_point = add_vec(ray.offset, ray.direction.times_factor(smallest_param))
            distance = sub_vec(ray.offset, intersect_point).sum()

            if nearest_object == self.source:
                return nearest_object.rgb.travel(DEGRADATION, distance)

            source_ray = self.get_ray_to_source(intersect_point)
            if (self.source_ray_visible(
                dir_in=ray.direction,
                dir_out=source_ray.direction,
                normal=nearest_object.get_normal(intersect_point)
            )):
                if (nearest_object.is_source):
                    return nearest_object.rgb.travel(DEGRADATION, distance) # 
                else:
                    rgb_source = self.trace_ray(source_ray, rev + 1)
                    return rgb_source.interpolate(nearest_object.rgb).travel(DEGRADATION, distance)
            else:
                return RGBI(nearest_object.rgb.vals, 0) # Shadow

            
    def get_ray_to_source(self, point: Vect) -> Ray:
        dir = sub_vec(self.source.offset, point)
        dir.normalise()
        return Ray(point, dir)
    
    def source_ray_visible(self, dir_in: Vect, dir_out: Vect, normal: Vect):
        alpha_1 = bm_to_am(angle_vec(dir_in.times_factor(-1), normal)) # needed so that in and out vector show are in the same direction
        alpha_2 = bm_to_am(angle_vec(dir_out, normal))

        if (alpha_1 < 90 and alpha_2 < 90) or (alpha_1 > 90 and alpha_2 > 90):
            return True
        else:
            return False
