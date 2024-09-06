import warnings
from typing import Union, List, Tuple
from typing_extensions import TypeAlias

import cv2
import numpy as np
from skimage.draw import polygon


NUMBER = Union[int, float]
VECTOR_LIKE: TypeAlias = Union[np.ndarray, List[NUMBER], Tuple[NUMBER, ...]]
MATRIX: TypeAlias = np.ndarray
VECTOR: TypeAlias = np.ndarray


def get_patch(frame: MATRIX, bbox: VECTOR_LIKE, copy: bool = True):
    x1, y1, x2, y2 = bbox
    patch = frame[y1:y2, x1:x2, ...]    
    return np.copy(patch) if copy else patch


def to_mask(bb: VECTOR, contours: np.ndarray):
    width, height = bb[2:] - bb[:2]
    mask = np.zeros((height, width), dtype=np.uint8)
    for cnt in contours:
        rr, cc = polygon(cnt[:, 1], cnt[:, 0])

        # FIXME: Polygon function sometimes exceeds the patch shape
        indices = (rr < height) & (cc < width)
        if len(indices) < len(rr):
            warnings.warn(f'Generated polygon exceeds patch shape')
        rr, cc = rr[indices], cc[indices]

        mask[rr, cc] = 255
    return mask


def get_masked_patch(frame: MATRIX, bbox: VECTOR, mask_contour: np.ndarray):
    patch = get_patch(frame, bbox, copy=False)
    mask = to_mask(bbox, mask_contour)
    return cv2.bitwise_and(patch, patch, mask=mask)


def area(bbox: VECTOR_LIKE):
    return (bbox[2] - bbox[0] + 1) * (bbox[3] - bbox[1] + 1)


def iou(bboxA: VECTOR_LIKE, bboxB: VECTOR_LIKE):
    xA = max(bboxA[0], bboxB[0])
    yA = max(bboxA[1], bboxB[1])
    xB = min(bboxA[2], bboxB[2])
    yB = min(bboxA[3], bboxB[3])

    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

    boxAArea = area(bboxA)
    boxBArea = area(bboxB)

    return interArea / float(boxAArea + boxBArea - interArea)
