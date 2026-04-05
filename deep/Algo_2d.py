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
    # Demo LP used by main() to generate the example simplex walk-through.
    A=np.array([[2.0, 1.0], [1.0, 2.0]], dtype=float),
    b=np.array([8.0, 10.0], dtype=float),
    c=np.array([3.0, 5.0], dtype=float),
)


def solve_simplex_with_trace(lp: LinearProgram) -> List[Tuple[float, float]]:
    """
    Run the tableau simplex method and record each BFS for a 2D max problem.

    The LP must be in standard form:
    maximize c^T x subject to A x <= b, b >= 0, x >= 0, y >= 0.
    """

    if lp.A.ndim != 2 or lp.A.shape[1] != 2:
        raise ValueError("solve_simplex_with_trace only supports 2D problems in x and y.")
    if lp.A.shape[0] == 0:
        raise ValueError("At least one inequality is required.")
    if lp.A.shape[0] > 8:
        raise ValueError("This solver supports at most 8 user-supplied inequalities.")
    if np.any(lp.b < -1e-9):
        raise ValueError("All right-hand sides must be non-negative for this simplex setup.")

    num_constraints = int(lp.A.shape[0])
    num_vars = 2 + num_constraints  # x, y, and one slack per inequality
    # Allocate one extra column for the RHS values.
    tableau = np.zeros((num_constraints + 1, num_vars + 1), dtype=float)
    tableau[:num_constraints, :2] = lp.A
    tableau[:num_constraints, 2 : 2 + num_constraints] = np.eye(num_constraints)
    tableau[:num_constraints, -1] = lp.b
    # The objective row stores -c so a negative entry signals an improving move.
    tableau[-1, :2] = -lp.c
    # Start with the slack variables as the basic variables.
    basis = list(range(2, 2 + num_constraints))

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


def build_plot_constraints(lp: LinearProgram) -> Tuple[np.ndarray, np.ndarray]:
    """Append x >= 0 and y >= 0 as -x <= 0 and -y <= 0 for geometry checks."""

    extra_a = np.array([[-1.0, 0.0], [0.0, -1.0]], dtype=float)
    extra_b = np.array([0.0, 0.0], dtype=float)
    # Nonnegativity is added here for geometry only; the simplex tableau already assumes it.
    full_a = np.vstack([lp.A, extra_a])
    full_b = np.concatenate([lp.b, extra_b])
    return full_a, full_b


def compute_feasible_vertices(lp: LinearProgram) -> List[Tuple[float, float]]:
    """Enumerate feasible vertices by intersecting every pair of boundary lines."""

    full_a, full_b = build_plot_constraints(lp)
    vertices: List[Tuple[float, float]] = []

    for i in range(len(full_a)):
        for j in range(i + 1, len(full_a)):
            matrix = np.array([full_a[i], full_a[j]], dtype=float)
            if abs(np.linalg.det(matrix)) < 1e-9:
                continue
            rhs = np.array([full_b[i], full_b[j]], dtype=float)
            point = np.linalg.solve(matrix, rhs)
            if np.all(full_a @ point <= full_b + 1e-8):
                candidate = (float(point[0]), float(point[1]))
                if not any(np.allclose(candidate, existing, atol=1e-7) for existing in vertices):
                    vertices.append(candidate)

    return vertices


def order_polygon(points: Sequence[Tuple[float, float]]) -> np.ndarray:
    """Sort polygon vertices counterclockwise for plotting."""

    pts = np.array(points, dtype=float)
    center = pts.mean(axis=0)
    angles = np.arctan2(pts[:, 1] - center[1], pts[:, 0] - center[0])
    return pts[np.argsort(angles)]


def plot_step(
    lp: LinearProgram,
    path: Sequence[Tuple[float, float]],
    step_index: int,
    title: str,
    outfile: str,
) -> None:
    """Plot feasible region plus simplex path up to a step, then save as PNG."""

    fig, ax = plt.subplots(figsize=(8, 6))

    vertices = compute_feasible_vertices(lp)
    if not vertices:
        raise ValueError("No feasible region found for the supplied inequalities.")

    polygon = order_polygon(vertices)
    ax.fill(
        polygon[:, 0],
        polygon[:, 1],
        color="steelblue",
        alpha=0.25,
        label="Feasible region",
    )

    max_x = max(max(point[0] for point in vertices), max(point[0] for point in path), 1.0)
    max_y = max(max(point[1] for point in vertices), max(point[1] for point in path), 1.0)
    x_line = np.linspace(0, max_x * 1.2 + 1.0, 400)

    styles = ["k-", "k--", "k-.", "k:", "b-", "b--", "g-", "g--"]
    for index, (row, rhs) in enumerate(zip(lp.A, lp.b)):
        a_coeff, b_coeff = row
        style = styles[index % len(styles)]
        # Handle the common nonvertical case as y = (rhs - ax) / b.
        if abs(b_coeff) > 1e-9:
            y_line = (rhs - a_coeff * x_line) / b_coeff
            mask = y_line >= -0.25
            ax.plot(
                x_line[mask],
                y_line[mask],
                style,
                lw=1,
                label=rf"${a_coeff:g}x + {b_coeff:g}y = {rhs:g}$",
            )
        elif abs(a_coeff) > 1e-9:
            # Vertical boundaries are drawn separately because they cannot be written as y = f(x).
            x_value = rhs / a_coeff
            ax.axvline(x=x_value, linestyle=style[-1], color=style[0], lw=1, label=rf"${a_coeff:g}x = {rhs:g}$")

    path_arr = np.array(path)
    ax.plot(path_arr[:, 0], path_arr[:, 1], "o-", color="darkorange", ms=10, lw=2, label="Simplex path")

    cx, cy = path[-1]
    ax.plot(cx, cy, "s", color="crimson", ms=12, label="Current BFS")

    for idx, (px, py) in enumerate(path):
        ax.annotate(str(idx), (px, py), textcoords="offset points", xytext=(6, 6), fontsize=11)

    ax.set_xlim(-0.2, max_x * 1.2 + 1.0)
    ax.set_ylim(-0.2, max_y * 1.2 + 1.0)
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
        # Slice the trace so each image shows the path discovered up to that iteration.
        partial_path = trace[: step + 1]
        outfile = os.path.join(out_dir, f"simplex_2d_step_{step + 1}.png")
        plot_step(PROBLEM, partial_path, step, labels[step] if step < len(labels) else f"iteration {step}", outfile)
        print(f"Wrote {outfile}")

    print("BFS sequence (x, y):", trace)


if __name__ == "__main__":
    main()
