from numpy.lib.utils import source
from .light_sources import LightSource
from .camera import SimpleCamera
from .coordinate_utils import *
from .light_sources import *
from .light_utils import *
from .objects import *

from math import inf

class Scenery:
    """
    Contains all Informations about the scenery (Objects, the Light Source, the camera)
    """

    objects: List[Object]
    source: LightSource
    camera: SimpleCamera

    def __init__(self, objects: List[Object], camera: SimpleCamera) -> None:
        """
        uses the first object which is a source as global source
        """
        self.objects = objects
        self.camera = camera
        for object in objects:
            if object.source_object is not None:
                self.source = object.source_object
                break
    
    def set_camera(self, camera: SimpleCamera):
        """
        Allows to change the camera later on
        """
        self.camera = camera

    def render_img_to_rgb_array(self) -> np.ndarray:
        """
        Renders the scene into a 3-dimensional array containing the rgb values for each pixel
        Also communicates the current status
        """

        print(f"rendering image with:\n\tresolution: {self.camera.width} x {self.camera.height}\n\t--------\n")
        
        # initialize sime variables
        data = np.zeros((self.camera.height, self.camera.width, 3), dtype=np.uint8)
        [x,y,n,percent] = [0,0,0,0]

        # how many rays must be finished to get to the next percent (used to display status)
        n_nxt_percent = self.camera.width * self.camera.height / 100

        # iterate over all primary rays and trace them
        for ray in self.camera.get_primary_rays():
            # trace ray and resolve returned light object
            data[y][x] = self.trace_ray(ray).resolve()

            # Computations for Percent output
            x = (x + 1) % self.camera.width
            if x == 0:
                y = (y + 1) % self.camera.height
            n = (n + 1) % n_nxt_percent
            if n == 0:
                print(f"\t{percent}%\n")
                percent = percent + 1

        # finished
        print("rendering finished\n")
        return data

    
    def trace_ray(self, ray: Ray, primary_ray: bool = True) -> Light:
        """
        Traces a single ray in the scene
        :param ray: the ray to trace
        :param primary_ray: is the ray a primary ray?
        """

        # determine closest intersect point (and object)
        [closest_param, closest_obj] = [inf , None]

        for object in self.objects:
            for param in object.get_intersection_params(ray):
                if param > 1e-6 and param < closest_param: # (param = 0 -> last hitpoint, but not really correct -> tolerance)
                    closest_param = param
                    closest_obj = object
        
        # determine how to proceed
        if closest_obj is None:
            # Ray never hits anything -> darkness
            return Light(rgb=BLACK, intensity=0)

        # compute distance and intersect Point
        intersect_point = ray.offset + (ray.direction * closest_param)
        distance = closest_param # travels 1 unit per param (since ray.direction is normalised)
        
        if closest_obj.source_object is not None:
            # let the light from the source travel the distance and return it
            return closest_obj.source_object.get_light_intensity(ray.offset)
        elif primary_ray:
            # continue tracing ray recursively and interpolate the returned light information with the one 
            # of the closest object, then let the light travel the distance to the start point
            dir = (self.source.offset - intersect_point)
                # TODO: catch that ray might be behind object when object is between viewer and source
            light_intensity = self.trace_ray(Ray(intersect_point, dir), False)
            return get_diffuse_surface_color(closest_obj.albedo, light_intensity, normalise(closest_obj.get_normal(intersect_point)), normalise(dir)).travel(distance)
        else:
            # if the ray hits and object and was already reflected by an object, it's a shadow ray
            return Light(BLACK, 0)


