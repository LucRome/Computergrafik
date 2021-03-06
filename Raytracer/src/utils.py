from raytracer.camera import SimpleCamera
from raytracer.trace_algorithm import Scenery
from pathlib import Path

import numpy as np

"""
Utility Functions (mainly for debugging)
"""

def test_single_pixel(scenery: Scenery, pixel_x: int, pixel_y: int) -> np.ndarray:
    """
    Only renders a single Pixel
    """
    [x,y] = [0,0]
    for ray in scenery.camera.get_primary_rays():
        if x != pixel_x or y != pixel_y:
            x = (x + 1) % scenery.camera.width
            if x == 0:
                y = (y + 1) % scenery.camera.height
        else:
            material = scenery.trace_ray(ray)
            rgb = material
            return rgb

DATA_DIR = Path(__file__).resolve().parent.joinpath('data')

def pad_int_3(x: int):
    """
    Pad an integer (`x`) into a string so that it the string has a length of at least 3
    Using leading zeros
    """
    if x < 10:
        return f"00{x}"
    elif x < 100:
        return f"0{x}"
    else:
        return str(x)


def print_rgb_array_to_file(data: np.ndarray, filename: str, width: np.int16, height: np.int16) -> None:
    """
    Prints the array that contains the rgb values into a file
    """
    if not DATA_DIR.exists():
        DATA_DIR.mkdir()
    data_file = open(DATA_DIR.joinpath(filename), mode='w')
    for y in range(0, height):
        for x in range(0, width):
            data_file.write(f" [{pad_int_3(data[y][x][0])}, {pad_int_3(data[y][x][1])}, {pad_int_3(data[y][x][2])}] ")
        data_file.write(" \n")
    data_file.close()


def save_rgb_array_to_file(scenery: Scenery, filename:str):
    """
    renders the scenery and saves the resulting array into a file
    """
    data = scenery.render_img_to_rgb_array()
    print_rgb_array_to_file(data, filename, scenery.camera.width, scenery.camera.height)