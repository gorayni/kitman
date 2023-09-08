import json
from functools import reduce
from operator import truediv
from pathlib import Path

import numpy as np

from kitman.data import DirPathsBuilder
from kitman.field_calibration import format_homography


def load_scaling_matrix(sars_filepath: Path):
    with sars_filepath.open(mode='r') as f:
        sampling_aspect_ratio = reduce(truediv, map(float, f.readline().split(':')))

    scaling_matrix = np.identity(3)
    if sampling_aspect_ratio > 1:
        scaling_matrix[0, 0] = 1 / sampling_aspect_ratio
    return scaling_matrix


def load_homographies(calibration_filepath: Path, transformation_matrix: np.ndarray = None):
    with calibration_filepath.open() as json_file:
        data = json.load(json_file)

    homographies = []
    for prediction in data['predictions']:
        homography_matrix = format_homography(prediction[0]['homography'])
        if transformation_matrix is not None:
            homography_matrix = homography_matrix @ transformation_matrix
        homographies.append({'matrix': homography_matrix,
                             'confidence': prediction[0]['confidence']})
    return homographies


def load_groundtruth_bboxes(bboxes_filepath: Path):
    with bboxes_filepath.open() as json_file:
        data = json.load(json_file)
    return data['predictions']


class FrameIndex:
    def __init__(self, half, frame_idx):
        self.half = half
        self.frame_idx = frame_idx


class MatchPaths(DirPathsBuilder):
    def __init__(self, match_path):
        super().__init__(match_path, {'calibrations': '{}_field_calib_ccbv.json',
                                      'frames': ['{}_HQ', 'frames', '{:05d}.jpg'],
                                      'predicted_segmentations': 'predicted_segmentation_{}.npy',
                                      'predicted_segmentations_bkg': 'predicted_segmentation_bkg_{}.npy',
                                      'sampling_aspect_ratio': 'sampling_aspect_ratio.txt',
                                      'segmentations': 'segmentation_results_{}_HQ.npy'
                                      })
        self.match = match_path
