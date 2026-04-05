"""
Combine the saved simplex step plots into one summary image.
"""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Iterable

import matplotlib.image as mpimg
import matplotlib.pyplot as plt


STEP_FILE_RE = re.compile(r"simplex_2d_step_(\d+)\.png$")


def step_sort_key(path: Path) -> int:
    """Extract the numeric step index from a saved plot filename."""
    # Pull the step number out of the filename so lexicographic ordering does not mis-sort it.
    match = STEP_FILE_RE.fullmatch(path.name)
    if match is None:
        raise ValueError(f"Unexpected step image name: {path.name}")
    return int(match.group(1))


def combine_images(image_paths: Iterable[Path], outfile: Path) -> None:
    """Combine simplex step images into a single summary image."""

    image_paths = list(image_paths)
    if not image_paths:
        raise FileNotFoundError("No simplex step images were provided.")

    # Lay out the saved step images in a compact grid.
    cols = min(3, len(image_paths))
    rows = math.ceil(len(image_paths) / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))

    if hasattr(axes, "ravel"):
        # A grid returns an array of axes; flatten it so the loop below stays simple.
        axes_list = list(axes.ravel())
    else:
        # A single subplot is already just one axis.
        axes_list = [axes]

    # Each subplot shows one previously generated simplex step image.
    for ax, image_path in zip(axes_list, image_paths):
        ax.imshow(mpimg.imread(image_path))
        ax.set_title(image_path.stem.replace("_", " "))
        ax.axis("off")

    for ax in axes_list[len(image_paths) :]:
        # Hide empty cells when the image count does not fill the last row.
        ax.axis("off")

    fig.suptitle("Simplex 2D Walk-Through", fontsize=16)
    fig.tight_layout()

    fig.savefig(outfile, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {outfile}")


def main() -> None:
    out_dir = Path(__file__).resolve().parent
    # Collect all step images from the current folder before combining them.
    image_paths = sorted(out_dir.glob("simplex_2d_step_*.png"), key=step_sort_key)

    if not image_paths:
        raise FileNotFoundError(
            "No simplex step images found. Run simplex_2d.py first to create them."
        )

    combine_images(image_paths, out_dir / "simplex_2d_all.png")


if __name__ == "__main__":
    main()
