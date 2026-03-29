"""
2D simplex method: visualize feasible region and successive basic feasible solutions.
Saves three PNG images for the first three tableau iterations (starting BFS + pivots).
"""


import os

import matplotlib.pyplot as plt
import numpy as np

# Maximize z = 3*x + 5*ys
# s.t.  2*x + y <= 8
#       x + 2*y <= 10
#       x, y >= 0


def solve_simplex_with_trace():
    """Tableau for max problem; columns: x, y, s1, s2 | RHS."""
    # Rows: constraints; last row: objective as z - 3x - 5y = 0  ->  [-3,-5,0,0|0] with z implicit
    tableau = np.array(
        [
            [2.0, 1.0, 1.0, 0.0, 8.0],
            [1.0, 2.0, 0.0, 1.0, 10.0],
            [-3.0, -5.0, 0.0, 0.0, 0.0],
        ],
        dtype=float,
    )
    m, n = 2, 4  # 2 constraints, 4 structural cols
    basis = [2, 3]  # s1, s2 (0-indexed column indices)

    def bfs_xy():
        x = np.zeros(4)
        for row, col in enumerate(basis):
            x[col] = tableau[row, -1]
        return float(x[0]), float(x[1])

    trace = [bfs_xy()]

    max_iter = 20
    for _ in range(max_iter):
        obj = tableau[-1, :n]
        # Max: enter most negative coefficient in z - sum c_i x_i row
        if obj.min() >= -1e-9:
            break
        pivot_col = int(obj.argmin())
        # Minimum ratio test
        ratios = []
        for r in range(m):
            a = tableau[r, pivot_col]
            rhs = tableau[r, -1]
            if a > 1e-9:
                ratios.append(rhs / a)
            else:
                ratios.append(np.inf)
        pivot_row = int(np.argmin(ratios))
        if not np.isfinite(ratios[pivot_row]):
            break

        piv = tableau[pivot_row, pivot_col]
        tableau[pivot_row, :] /= piv
        for r in range(m + 1):
            if r != pivot_row:
                tableau[r, :] -= tableau[r, pivot_col] * tableau[pivot_row, :]
        basis[pivot_row] = pivot_col
        trace.append(bfs_xy())

    return trace


def plot_step(xy_points, step_index, title_suffix, outfile):
    fig, ax = plt.subplots(figsize=(8, 6))

    # Feasible region: 2x+y<=8, x+2y<=10, x>=0, y>=0
    xs = np.linspace(0, 5, 200)
    y1 = np.maximum(0, 8 - 2 * xs)
    y2 = np.maximum(0, (10 - xs) / 2)
    y_upper = np.minimum(y1, y2)
    ax.fill_between(xs, 0, y_upper, where=(y_upper >= 0), alpha=0.25, color="steelblue", label="Feasible region")

    # Constraint lines
    x_line = np.array([0, 4.5])
    ax.plot(x_line, 8 - 2 * x_line, "k-", lw=1, label=r"$2x+y=8$")
    ax.plot(x_line, (10 - x_line) / 2, "k--", lw=1, label=r"$x+2y=10$")

    path = np.array(xy_points)
    ax.plot(path[:, 0], path[:, 1], "o-", color="darkorange", ms=10, lw=2, label="Simplex path")

    cx, cy = xy_points[-1]
    ax.plot(cx, cy, "s", color="crimson", ms=12, label="Current BFS")

    for i, (px, py) in enumerate(xy_points):
        ax.annotate(f"{i}", (px, py), textcoords="offset points", xytext=(6, 6), fontsize=11)

    ax.set_xlim(-0.2, 5)
    ax.set_ylim(-0.2, 6)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.set_title(f"Simplex step {step_index + 1}: {title_suffix}")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", fontsize=9)

    fig.tight_layout()
    fig.savefig(outfile, dpi=150)
    plt.close(fig)


def main():
    trace = solve_simplex_with_trace()
    out_dir = os.path.dirname(os.path.abspath(__file__))

    labels = [
        "initial BFS $(x,y)=(0,0)$",
        "after 1st pivot",
        "optimal vertex",
    ]
    for k in range(3):
        prefix = trace[: k + 1]
        outfile = os.path.join(out_dir, f"simplex_2d_step_{k + 1}.png")
        plot_step(prefix, k, labels[k] if k < len(labels) else f"iteration {k}", outfile)
        print(f"Wrote {outfile}")

    print("BFS sequence (x, y):", trace)


if __name__ == "__main__":
    main()
