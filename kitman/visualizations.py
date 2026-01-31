import warnings

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib.patches import Arc, Circle, Rectangle
from skimage import io
from skimage.draw import polygon
from typing import TypedDict, Sequence, Optional, Tuple
from matplotlib.patches import Patch

REPRESENTATION_WIDTH = 105
REPRESENTATION_HEIGHT = 68
REPRESENTATION_CHANNEL = 3


def draw_mask(frame, bb, contours, color=None):
    x1, y1, x2, y2 = bb

    if color is None:
        color = 255

    patch = frame[y1:y2, x1:x2, ...]
    for cnt in contours:
        rr, cc = polygon(cnt[:, 1], cnt[:, 0])

        # FIXME: Polygon function sometimes exceeds the patch shape
        original_rr_size = len(rr)
        rr = np.minimum(rr, patch.shape[0] - 1)
        cc = np.minimum(cc, patch.shape[1] - 1)

        if len(rr) < original_rr_size:
            warnings.warn(f"Generated polygon exceeds patch shape")

        patch[rr, cc, ...] = color


def draw_soccer_field(figsize=None, ax=None):
    if not figsize:
        figsize = (10, 5)

    if not ax:
        fig, ax = plt.subplots(figsize=figsize)

    ax.add_patch(
        Rectangle(
            (0, 0),
            REPRESENTATION_WIDTH,
            REPRESENTATION_HEIGHT,
            linewidth=3,
            edgecolor="w",
            facecolor="g",
        )
    )
    ax.add_patch(
        Rectangle(
            (0, 0),
            REPRESENTATION_WIDTH / 2,
            REPRESENTATION_HEIGHT,
            linewidth=3,
            edgecolor="w",
            facecolor="g",
        )
    )

    RADIUS = 9.15
    ax.add_patch(
        Circle(
            (REPRESENTATION_WIDTH / 2, REPRESENTATION_HEIGHT / 2),
            RADIUS,
            linewidth=2,
            edgecolor="w",
            facecolor="none",
        )
    )
    ax.add_patch(
        Arc(
            (11, REPRESENTATION_HEIGHT / 2),
            2 * RADIUS,
            2 * RADIUS,
            theta1=-55,
            theta2=55,
            linewidth=2,
            color="w",
        )
    )
    ax.add_patch(
        Arc(
            (REPRESENTATION_WIDTH - 11, REPRESENTATION_HEIGHT / 2),
            2 * RADIUS,
            2 * RADIUS,
            theta1=125,
            theta2=235,
            linewidth=2,
            color="w",
        )
    )

    CORNER_RADIUS = 2
    ax.add_patch(
        Arc(
            (0, 0),
            CORNER_RADIUS,
            CORNER_RADIUS,
            theta1=0,
            theta2=90,
            linewidth=2,
            color="w",
        )
    )
    ax.add_patch(
        Arc(
            (0, REPRESENTATION_HEIGHT),
            CORNER_RADIUS,
            CORNER_RADIUS,
            theta1=270,
            theta2=360,
            linewidth=2,
            color="w",
        )
    )

    ax.add_patch(
        Arc(
            (REPRESENTATION_WIDTH, 0),
            CORNER_RADIUS,
            CORNER_RADIUS,
            theta1=90,
            theta2=1800,
            linewidth=2,
            color="w",
        )
    )
    ax.add_patch(
        Arc(
            (REPRESENTATION_WIDTH, REPRESENTATION_HEIGHT),
            CORNER_RADIUS,
            CORNER_RADIUS,
            theta1=180,
            theta2=270,
            linewidth=2,
            color="w",
        )
    )

    PENALTY_AREA_WIDTH = 16.5
    PENALTY_AREA_HEIGHT = 40.32
    ax.add_patch(
        Rectangle(
            (0, (REPRESENTATION_HEIGHT - PENALTY_AREA_HEIGHT) / 2),
            PENALTY_AREA_WIDTH,
            PENALTY_AREA_HEIGHT,
            linewidth=3,
            edgecolor="w",
            facecolor="g",
        )
    )
    ax.add_patch(
        Rectangle(
            (
                REPRESENTATION_WIDTH - PENALTY_AREA_WIDTH,
                (REPRESENTATION_HEIGHT - PENALTY_AREA_HEIGHT) / 2,
            ),
            PENALTY_AREA_WIDTH,
            PENALTY_AREA_HEIGHT,
            linewidth=3,
            edgecolor="w",
            facecolor="g",
        )
    )

    GOAL_AREA_WIDTH = 5.5
    GOAL_AREA_HEIGHT = 18.32
    ax.add_patch(
        Rectangle(
            (0, (REPRESENTATION_HEIGHT - GOAL_AREA_HEIGHT) / 2),
            GOAL_AREA_WIDTH,
            GOAL_AREA_HEIGHT,
            linewidth=3,
            edgecolor="w",
            facecolor="g",
        )
    )
    ax.add_patch(
        Rectangle(
            (
                REPRESENTATION_WIDTH - GOAL_AREA_WIDTH,
                (REPRESENTATION_HEIGHT - GOAL_AREA_HEIGHT) / 2,
            ),
            GOAL_AREA_WIDTH,
            GOAL_AREA_HEIGHT,
            linewidth=3,
            edgecolor="w",
            facecolor="g",
        )
    )

    ax.set_xlim([0, REPRESENTATION_WIDTH])
    ax.set_ylim([0, REPRESENTATION_HEIGHT])
    ax.set_aspect("equal")

    if "fig" in locals():
        return fig, ax


def sample_colors_from_cmap(N, cmap_name="hsv"):
    cmap = cm.get_cmap(cmap_name)
    colors = cmap(np.linspace(0, 1, N))
    return colors


class FrameDataDict(TypedDict):
    frame_path: str
    player_categories: Sequence
    segmentation_patches: Sequence[polygon]


def plot_players_overlaid(
    data: FrameDataDict,
    player_colors: Optional[dict] = None,
    figsize=(15, 7.5),
    title: Optional[str] = None,
    ax=None,
    fontsize: int = 14,
) -> Optional[Tuple[plt.Figure, plt.Axes]]:
    frame = io.imread(data["frame_path"])

    if not ax:
        fig, ax = plt.subplots(figsize=figsize)

    if title:
        ax.set_title(title, fontweight="bold", fontsize=fontsize)

    ax.imshow(frame)

    categories = np.unique(data["player_categories"])

    if not player_colors:
        num_player_categories = len(categories)
        player_colors = {
            cat: col
            for cat, col in zip(
                categories, sample_colors_from_cmap(num_player_categories)
            )
        }

    patches = {c: [] for c in data["segmentation_patches"]}
    for c, p in zip(data["player_categories"], data["segmentation_patches"]):
        patches[c].append(p)

    for i in patches.keys():
        p = PatchCollection(patches[i], color=player_colors[i], alpha=0.4)
        ax.add_collection(p)

    if "fig" in locals():
        fig.tight_layout()
        return fig, ax
