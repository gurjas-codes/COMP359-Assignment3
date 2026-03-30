"""
Simple, readable walk-through of the 2D simplex method for a class project.
Solves a tiny LP, logs each basic feasible solution (BFS), and saves plots that
show how the algorithm walks across the feasible region.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Sequence, Tuple

import matplotlib.pyplot as plt
import numpy as np

# Problem statement (keep it close to the code we operate on).
# Maximize z = 3x + 5y
# subject to: 2x + y <= 8,   x + 2y <= 10,   x >= 0, y >= 0


@dataclass(frozen=True)
class LinearProgram:
    """Tiny LP in max form: maximize c^T x subject to Ax <= b."""

    A: np.ndarray
    b: np.ndarray
    c: np.ndarray


PROBLEM = LinearProgram(
    A=np.array([[2.0, 1.0], [1.0, 2.0]], dtype=float),
    b=np.array([8.0, 10.0], dtype=float),
    c=np.array([3.0, 5.0], dtype=float),
)


def solve_simplex_with_trace(lp: LinearProgram) -> List[Tuple[float, float]]:
    """
    Run the tableau simplex method and record each BFS.

    Tableau columns: x, y, s1, s2 | RHS. The last row stores z - c^T x = 0.
    """

    tableau = np.array(
        [
            [lp.A[0, 0], lp.A[0, 1], 1.0, 0.0, lp.b[0]],
            [lp.A[1, 0], lp.A[1, 1], 0.0, 1.0, lp.b[1]],
            [-lp.c[0], -lp.c[1], 0.0, 0.0, 0.0],
        ],
        dtype=float,
    )

    num_constraints = 2
    num_vars = 4  # x, y, s1, s2
    basis = [2, 3]  # start with slack variables in the basis

    def current_xy() -> Tuple[float, float]:
        """Read the basic variables out of the tableau into (x, y)."""
        solution = np.zeros(num_vars)
        for row, col in enumerate(basis):
            solution[col] = tableau[row, -1]
        return float(solution[0]), float(solution[1])

    bfs_trace: List[Tuple[float, float]] = [current_xy()]

    max_iter = 20
    for _ in range(max_iter):
        obj_row = tableau[-1, :num_vars]

        # Entering variable: most negative reduced cost (maximization).
        if obj_row.min() >= -1e-9:
            break  # optimal
        pivot_col = int(obj_row.argmin())

        # Leaving variable: minimum ratio test RHS / pivot column.
        ratios: List[float] = []
        for r in range(num_constraints):
            coeff = tableau[r, pivot_col]
            rhs = tableau[r, -1]
            ratios.append(rhs / coeff if coeff > 1e-9 else np.inf)

        pivot_row = int(np.argmin(ratios))
        if not np.isfinite(ratios[pivot_row]):
            break  # unbounded in this direction

        pivot_val = tableau[pivot_row, pivot_col]
        tableau[pivot_row, :] /= pivot_val
        for r in range(num_constraints + 1):
            if r != pivot_row:
                tableau[r, :] -= tableau[r, pivot_col] * tableau[pivot_row, :]

        basis[pivot_row] = pivot_col
        bfs_trace.append(current_xy())

    return bfs_trace


def plot_step(path: Sequence[Tuple[float, float]], step_index: int, title: str, outfile: str) -> None:
    """Plot feasible region plus simplex path up to a step, then save as PNG."""

    fig, ax = plt.subplots(figsize=(8, 6))

    xs = np.linspace(0, 5, 200)
    y1 = np.maximum(0, PROBLEM.b[0] - 2 * xs)
    y2 = np.maximum(0, (PROBLEM.b[1] - xs) / 2)
    y_upper = np.minimum(y1, y2)
    ax.fill_between(xs, 0, y_upper, where=(y_upper >= 0), alpha=0.25, color="steelblue", label="Feasible region")

    x_line = np.array([0, 4.5])
    ax.plot(x_line, 8 - 2 * x_line, "k-", lw=1, label=r"$2x + y = 8$")
    ax.plot(x_line, (10 - x_line) / 2, "k--", lw=1, label=r"$x + 2y = 10$")

    path_arr = np.array(path)
    ax.plot(path_arr[:, 0], path_arr[:, 1], "o-", color="darkorange", ms=10, lw=2, label="Simplex path")

    cx, cy = path[-1]
    ax.plot(cx, cy, "s", color="crimson", ms=12, label="Current BFS")

    for idx, (px, py) in enumerate(path):
        ax.annotate(str(idx), (px, py), textcoords="offset points", xytext=(6, 6), fontsize=11)

    ax.set_xlim(-0.2, 5)
    ax.set_ylim(-0.2, 6)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.set_title(f"Simplex step {step_index + 1}: {title}")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", fontsize=9)

    fig.tight_layout()
    fig.savefig(outfile, dpi=150)
    plt.close(fig)


def main() -> None:
    trace = solve_simplex_with_trace(PROBLEM)
    out_dir = os.path.dirname(os.path.abspath(__file__))

    labels = [
        "initial BFS (x,y)=(0,0)",
        "after 1st pivot",
        "optimal vertex",
    ]

    for step in range(3):
        partial_path = trace[: step + 1]
        outfile = os.path.join(out_dir, f"simplex_2d_step_{step + 1}.png")
        plot_step(partial_path, step, labels[step] if step < len(labels) else f"iteration {step}", outfile)
        print(f"Wrote {outfile}")

    print("BFS sequence (x, y):", trace)


if __name__ == "__main__":
    main()
