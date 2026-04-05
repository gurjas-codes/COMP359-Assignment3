"""
Combine the saved simplex step plots into one summary image.
"""

from __future__ import annotations

import math
import re
from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt


STEP_FILE_RE = re.compile(r"simplex_2d_step_(\d+)\.png$")


def step_sort_key(path: Path) -> int:
    """Extract the numeric step index from a saved plot filename."""
    match = STEP_FILE_RE.fullmatch(path.name)
    if match is None:
        raise ValueError(f"Unexpected step image name: {path.name}")
    return int(match.group(1))


def main() -> None:
    out_dir = Path(__file__).resolve().parent
    image_paths = sorted(out_dir.glob("simplex_2d_step_*.png"), key=step_sort_key)

    if not image_paths:
        raise FileNotFoundError(
            "No simplex step images found. Run simplex_2d.py first to create them."
        )

    cols = min(3, len(image_paths))
    rows = math.ceil(len(image_paths) / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))

    if hasattr(axes, "ravel"):
        axes_list = list(axes.ravel())
    else:
        axes_list = [axes]

    for ax, image_path in zip(axes_list, image_paths):
        ax.imshow(mpimg.imread(image_path))
        ax.set_title(image_path.stem.replace("_", " "))
        ax.axis("off")

    for ax in axes_list[len(image_paths) :]:
        ax.axis("off")

    fig.suptitle("Simplex 2D Walk-Through", fontsize=16)
    fig.tight_layout()

    outfile = out_dir / "simplex_2d_all.png"
    fig.savefig(outfile, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {outfile}")


if __name__ == "__main__":
    main()
