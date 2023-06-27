import numpy as np

from kitman.field_calibration import calculate_player_position, \
    DIM_IMAGE, \
    GOAL_CENTERS

DIM_TERRAIN = (68, 105, 3)


def meter2radar(points2D, dim_terrain=None, dim_image=None):
    if dim_terrain is None:
        dim_terrain = DIM_TERRAIN

    if dim_image is None:
        dim_image = DIM_IMAGE

    dim_image = dim_image[:2][-1::-1]
    dim_terrain = dim_terrain[:2][-1::-1]
    return dim_image * (0.95 * points2D / dim_terrain + 0.5 + 0.025)


def calculate_radar_position(bbox, homography):
    projected_point = calculate_player_position(bbox, homography)
    return meter2radar(projected_point, DIM_TERRAIN, DIM_IMAGE)
