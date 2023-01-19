from enum import Enum, auto

from PIL.Image import Image


class Algo(Enum):
    RGB_SUM = auto()
    R = auto()
    G = auto()
    B = auto()
    BW = auto()


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
