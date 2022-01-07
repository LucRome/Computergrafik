import numpy as np
from raytracer.trace_algorithm import Scenery
from PIL import Image

from time import time_ns, struct_time
"""
Utility Functions
"""

def save_as_img(path: str, scenery: Scenery) -> None:
    """
    Renders the Scenery and saves it as an image file (e.g. png)
    """
    data = scenery.render_img_to_rgb_array()
    img = Image.fromarray(data, mode='RGB')
    img.save(path)

def save_as_img_timed(path: str, scenery: Scenery) -> None:
    """
    Renders the Scenery and saves it as an image file (e.g. png)
    Also tracks how long the process of rendering took
    """
    time_start = time_ns()
    data = scenery.render_img_to_rgb_array()
    dt = time_ns() - time_start
    [h,m,s,ms] = [np.floor(dt/(1e9*3600)), np.floor(dt/(1e9*60))%60, np.floor(dt/1e9)%60, np.floor(dt/1e6)%1e3]
    print(f"Rendering took: {h}:{m}:{s}:{ms} (h:m:s:ms)\n")
    # save image
    Image.fromarray(data, mode='RGB').save(path)