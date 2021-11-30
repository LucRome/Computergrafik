from raytracer.camera import SimpleCamera
from raytracer.coordinate_utils import *
from raytracer.materials import *
from raytracer.objects import *

from math import inf
class Scenery:
    objects: List[Object]
    camera: SimpleCamera
    light_degradation: np.float16
    max_depth: int
    source: LightSphere

    def __init__(self, objects: List[Object], camera: SimpleCamera, max_depth: int, light_degradation: np.float16) -> None:
        """
        uses the first object which is a source as global source
        """
        self.objects = objects
        self.camera = camera
        self.max_depth = max_depth
        self.light_degradation = light_degradation
        for object in objects:
            if object.is_source:
                self.source = object
                break
    
    def set_camera(self, camera: SimpleCamera):
        self.camera = camera

    def render_img_to_rgb_array(self) -> np.ndarray:
        print(f"rendering image with:\n\tresolution: {self.camera.width} x {self.camera.height}\n\tdepth: {self.max_depth}\n\t--------\n")
        data = np.zeros((self.camera.height, self.camera.width, 3), dtype=np.uint8)
        [x,y,n,percent] = [0,0,0,0]
        n_nxt_percent = self.camera.width * self.camera.height / 100
        for ray in self.camera.get_primary_rays():
            data[y][x] = self.trace_ray(ray).to_rgb_array()
            x = (x + 1) % self.camera.width
            if x == 0:
                y = (y + 1) % self.camera.height
            n = (n + 1) % n_nxt_percent
            if n == 0:
                print(f"\t{percent}%\n")
                percent = percent + 1
        print("rendering finished\n")
        return data

    
    def trace_ray(self, ray: Ray, depth: int = 0) -> Material:
        if depth > self.max_depth:
            return SHADOW_MATERIAL

        # determine closest intersect point (and object)
        [closest_param, closest_obj] = [inf , None]

        for object in self.objects:
            for param in object.get_intersection_params(ray):
                if param > 1e-6 and param < closest_param: # (param = 0 -> last hitpoint, but not really correct -> tolerance)
                    closest_param = param
                    closest_obj = object
        
        # determine how to proceed
        if closest_obj is None:
            return SHADOW_MATERIAL

        # compute distance and intersect Point
        intersect_point = np.add(ray.offset, np.multiply(ray.direction, closest_param))
        distance = closest_param # travels 1 unit per param (since ray.direction is normalised)
        
        if closest_obj.is_source:
            # let the light from the source travel the distance and return it
            return closest_obj.material.travel(distance, self.light_degradation)
        else:
            # continue tracing ray recursively and interpolate the returned light information with the one 
            # of the closest object, then let the light travel the distance to the start point
            dir = np.subtract(self.source.offset, intersect_point)
                # TODO: catch that ray might be behind object when object is between viewer and source
            mat = self.trace_ray(Ray(intersect_point, dir), depth + 1)
            return closest_obj.material.interpolate(mat).travel(distance, self.light_degradation)


