import numpy as np

REPRESENTATION_HEIGHT = 32
REPRESENTATION_WIDTH = 64
REPRESENTATION_CHANNEL = 3

DIM_TERRAIN = (68, 105, REPRESENTATION_CHANNEL)
DIM_IMAGE = (REPRESENTATION_HEIGHT,
             REPRESENTATION_WIDTH,
             REPRESENTATION_CHANNEL)

GOAL_CENTERS = np.asarray([[0, 16], [64, 16]])


def meter2radar(point2D, dim_terrain, dim_image):
    return np.array([dim_image[1] * ((0.95 * point2D[0] / dim_terrain[1]) + 0.5 + 0.025),
                     dim_image[0] * ((0.95 * point2D[1] / dim_terrain[0]) + 0.5 + 0.025)])
