from enum import Enum

from PIL.Image import Image


class Algo(Enum):
    RGB_SUM = 'RGBsum'
    R = 'R'
    G = 'G'
    B = 'B'
    BW = 'BW'


def apply_algo(img: Image, algo: Algo) -> Image:
    """Applies chosen color mode to the image"""

    if algo is Algo.RGB_SUM:
        return img.convert("RGB")
    elif algo is Algo.R:
        return adjust_to_color(img, 0)
    elif algo is Algo.G:
        return adjust_to_color(img, 1)
    elif algo is Algo.B:
        return adjust_to_color(img, 2)
    elif algo is Algo.BW:
        # TODO: check if this actually works with black/white images
        return img.convert("RGB")
    raise AssertionError  # Should never occur


def adjust_to_color(img, pos):
    """Takes an image and returns a new image with the same size
    The new image only uses either the R, G or B values of the original image"""
    # TODO: it seems like this does not create a new image? In that case the docstring and usages should be changed

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            val = img.getpixel((x, y))[pos]
            img.putpixel((x, y), (val, val, val))
    return img

