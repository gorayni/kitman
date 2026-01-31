from typing import Union, List, Tuple
from typing_extensions import TypeAlias

import numpy as np

REPRESENTATION_HEIGHT = 32
REPRESENTATION_WIDTH = 64
REPRESENTATION_CHANNEL = 3

DIM_IMAGE = (REPRESENTATION_HEIGHT, REPRESENTATION_WIDTH, REPRESENTATION_CHANNEL)

CENTER_COORDS = np.asarray([REPRESENTATION_WIDTH // 2, REPRESENTATION_HEIGHT // 2])

GOAL_CENTERS = np.asarray([[0, 16], [64, 16]])

NUMBER = Union[int, float]
VECTOR: TypeAlias = np.ndarray
MATRIX: TypeAlias = np.ndarray
VECTOR_LIKE: TypeAlias = Union[np.ndarray, List[NUMBER], Tuple[NUMBER, ...]]


def unproject_image_point(homography: MATRIX, point2D: VECTOR):
    pitchpoint = homography @ point2D
    return pitchpoint / (pitchpoint[2] + 1e-8)


def format_homography(homography: VECTOR):
    homography = np.reshape(homography, (3, 3))
    homography = homography / homography[2, 2]
    return np.linalg.inv(homography)


def calculate_player_position(
    bbox: VECTOR_LIKE, homography: MATRIX, shape: Tuple[int, ...] = None
):
    x, y = (bbox[0] + bbox[2]) / 2, bbox[3]
    if shape is not None:
        x = x / shape[1] - 0.5
        y = y / shape[0] - 0.5

    projection_point = np.array([x, y, 1])
    return unproject_image_point(homography, projection_point)[:2]


def to_coords(point_2d: VECTOR, dim_image: VECTOR_LIKE):
    point_2d = point_2d + 0.5
    point_2d[0] *= dim_image[1]
    point_2d[1] *= dim_image[0]
    return point_2d
