from pathlib import Path
from typing import Dict, \
    List

import numpy as np

POINTREND_PERSON_ID = [0]


class SegmentedPlayer:
    def __init__(self, bb, mask_cnts, class_id, score):
        self.bb = bb
        self.mask_cnts = mask_cnts
        self.class_id = class_id
        self.score = score

    @staticmethod
    def to_segmented_players(seg_img: Dict, min_score: float = 0.0, filtered_class_ids: List[int] = None):
        if filtered_class_ids:
            return [SegmentedPlayer(bb, mask, class_id, score) for bb, mask, class_id, score in
                    zip(seg_img['boxes'], seg_img['masks'], seg_img['class_ids'], seg_img['scores'])
                    if class_id in filtered_class_ids and score >= min_score]

        return [SegmentedPlayer(bb, mask, class_id, score) for bb, mask, class_id, score in
                zip(seg_img['boxes'], seg_img['masks'], seg_img['class_ids'], seg_img['scores'])]

    @staticmethod
    def load(segmentation_fpath: Path, min_score: float = 0.0, class_id_filters: List[int] = None):
        segmented_images = np.load(segmentation_fpath, allow_pickle=True)
        return [SegmentedPlayer.to_segmented_players(s, min_score, class_id_filters) for s in segmented_images]
