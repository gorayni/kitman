import cv2
import numpy as np
from PIL import Image
from skimage import io
from skimage.morphology import binary_erosion, disk

from kitman.regions import get_patch, to_mask


def remove_players_background(frame_path, segmented_players, erosion_disk_radius=2):
    img = io.imread(frame_path)
    players = []
    for i, s in enumerate(segmented_players):
        patch = get_patch(img, s.bb, copy=False)
        mask = to_mask(s.bb, s.mask_cnts)

        eroded_mask = np.zeros(mask.shape, dtype=np.uint8)
        binary_erosion(mask, disk(erosion_disk_radius), out=eroded_mask)

        mask = 255 * eroded_mask
        masked_patch = cv2.bitwise_and(patch, patch, mask=mask)

        r, g, b = cv2.split(masked_patch)
        players.append(Image.fromarray(cv2.merge([r, g, b, mask], 4), "RGBA"))
    return players
