import numpy as np

REPRESENTATION_HEIGHT = 32
REPRESENTATION_WIDTH = 64
REPRESENTATION_CHANNEL = 3

DIM_TERRAIN = (68, 105, REPRESENTATION_CHANNEL)
DIM_IMAGE = (REPRESENTATION_HEIGHT,
             REPRESENTATION_WIDTH,
             REPRESENTATION_CHANNEL)

GOAL_CENTERS = np.asarray([[0, 16], [64, 16]])


def meter2radar(points2D, dim_terrain=None, dim_image=None):
    if dim_terrain is None:
        dim_terrain = DIM_TERRAIN

    if dim_image is None:
        dim_image = DIM_IMAGE

    dim_image = dim_image[:2][-1::-1]
    dim_terrain = dim_terrain[:2][-1::-1]
    return dim_image * (0.95 * points2D / dim_terrain + 0.5 + 0.025)
