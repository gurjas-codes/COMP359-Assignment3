"""
Gurjas — Higher-Dimensional Visualization

Visualizes higher-dimensional linear programming problems in 2D using:
  1. PCA (Principal Component Analysis) — reduces high dimensions to 2D
  2. Parallel Coordinates Plot — shows high-dimensional patterns
  3. Correlation Heatmap — shows relationships between dimensions

Also optionally visualizes Japneet's network LP (long15.mps) variable
distribution if the data file is available.

Usage:
    pip install scikit-learn
    python higher_dim_viz.py
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.optimize import linprog

# ---------------------------------------------------------------------------
# Output directory setup
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = SCRIPT_DIR  # save PNGs next to the script


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


# ===========================================================================
# Part 1 — Build and solve a higher-dimensional LP
# ===========================================================================

def build_higher_dim_lp():
    """
    Construct a 5-variable, 8-constraint LP to demonstrate higher dimensions.

    Maximize  z = 5x1 + 4x2 + 3x3 + 7x4 + 2x5
    subject to:
        2x1 +  x2 + 3x3 +  x4 + 2x5 <= 30      (resource A)
         x1 + 3x2 +  x3 + 2x4 +  x5 <= 25      (resource B)
        3x1 + 2x2 + 2x3 + 3x4 + 3x5 <= 40      (resource C)
         x1 +  x2 +  x3 +  x4 +  x5 <= 20      (total capacity)
        4x1 +  x2 +  x3 + 2x4 +  x5 <= 35      (resource D)
         x1 + 2x2 + 4x3 +  x4 + 2x5 <= 28      (resource E)
        2x1 + 3x2 +  x3 + 4x4 +  x5 <= 32      (resource F)
         x1 +  x2 + 2x3 + 2x4 + 3x5 <= 22      (resource G)
        x1, x2, x3, x4, x5 >= 0

    Returns the constraint matrix A, RHS vector b, objective c, and the
    optimal solution vector x*.
    """

    # Constraint coefficient matrix  (8 constraints × 5 variables)
    A = np.array([
        [2, 1, 3, 1, 2],
        [1, 3, 1, 2, 1],
        [3, 2, 2, 3, 3],
        [1, 1, 1, 1, 1],
        [4, 1, 1, 2, 1],
        [1, 2, 4, 1, 2],
        [2, 3, 1, 4, 1],
        [1, 1, 2, 2, 3],
    ], dtype=float)

    b = np.array([30, 25, 40, 20, 35, 28, 32, 22], dtype=float)

    # Objective: maximize  c^T x  ⟹  scipy minimizes, so negate c.
    c = np.array([5, 4, 3, 7, 2], dtype=float)

    result = linprog(-c, A_ub=A, b_ub=b, method="highs")

    if not result.success:
        print(f"Warning: LP solver did not find an optimal solution ({result.message})")

    print("=" * 55)
    print("HIGHER-DIMENSIONAL LP  (5 variables, 8 constraints)")
    print("=" * 55)
    print(f"Objective:  maximize z = 5x1 + 4x2 + 3x3 + 7x4 + 2x5")
    print(f"Optimal x:  {np.round(result.x, 4)}")
    print(f"Max z:      {-result.fun:.4f}")

    # Slack values for each constraint
    slacks = b - A @ result.x
    print("\nConstraint slack values:")
    labels = ["A", "B", "C", "D (cap)", "E", "F", "G", "H"]
    for i, (s, lbl) in enumerate(zip(slacks, labels)):
        binding = "  (binding)" if abs(s) < 1e-6 else ""
        print(f"  Resource {lbl}: slack = {s:.4f}{binding}")

    return A, b, c, result.x


# ===========================================================================
# Part 2 — Sample feasible points for visualization
# ===========================================================================

def sample_feasible_points(A, b, n_samples=500, seed=42):
    """
    Generate random feasible points inside the polytope Ax <= b, x >= 0
    by rejection sampling. These points let us scatter-plot the feasible
    region when projected to 2D.
    """

    rng = np.random.default_rng(seed)
    n_vars = A.shape[1]

    # Upper bound per variable: minimum of b_i / A_ij for positive A_ij
    upper = np.full(n_vars, np.inf)
    for j in range(n_vars):
        for i in range(A.shape[0]):
            if A[i, j] > 1e-9:
                upper[j] = min(upper[j], b[i] / A[i, j])
    upper = np.minimum(upper, 50.0)  # safety cap

    points = []
    attempts = 0
    max_attempts = n_samples * 200

    while len(points) < n_samples and attempts < max_attempts:
        x = rng.uniform(0, upper, size=n_vars)
        if np.all(A @ x <= b + 1e-9):
            points.append(x)
        attempts += 1

    points = np.array(points)
    print(f"\nSampled {len(points)} feasible points ({attempts} attempts)")
    return points


# ===========================================================================
# Visualization 1 — PCA projection to 2D
# ===========================================================================

def plot_pca(points, optimal, A, b, c):
    """
    Use PCA to project the 5D feasible points (and the optimum) onto 2D,
    then scatter-plot them coloured by objective value.
    """

    scaler = StandardScaler()
    scaled = scaler.fit_transform(points)

    pca = PCA(n_components=2)
    projected = pca.fit_transform(scaled)

    # Project the optimal point into the same PCA space
    opt_scaled = scaler.transform(optimal.reshape(1, -1))
    opt_proj = pca.transform(opt_scaled)[0]

    # Objective value at each point for colouring
    obj_vals = points @ c

    fig, ax = plt.subplots(figsize=(10, 8))

    scatter = ax.scatter(
        projected[:, 0], projected[:, 1],
        c=obj_vals, cmap="viridis", alpha=0.6, s=18, edgecolors="none",
    )
    cbar = fig.colorbar(scatter, ax=ax, pad=0.02)
    cbar.set_label("Objective value  z = 5x₁+4x₂+3x₃+7x₄+2x₅", fontsize=10)

    # Mark optimal
    ax.scatter(
        opt_proj[0], opt_proj[1],
        color="red", s=180, marker="*", zorder=5,
        edgecolors="black", linewidths=0.8,
        label=f"Optimal  z = {c @ optimal:.2f}",
    )

    # Explained variance annotation
    ev = pca.explained_variance_ratio_
    ax.set_xlabel(f"PC 1  ({ev[0]*100:.1f}% variance)", fontsize=11)
    ax.set_ylabel(f"PC 2  ({ev[1]*100:.1f}% variance)", fontsize=11)
    ax.set_title("PCA Projection of 5D Feasible Region onto 2D", fontsize=13)
    ax.legend(fontsize=10, loc="upper left")
    ax.grid(True, alpha=0.3)

    # Show component loadings as text
    loadings_text = "PCA loadings (PC1 / PC2):\n"
    var_names = ["x₁", "x₂", "x₃", "x₄", "x₅"]
    for j, name in enumerate(var_names):
        loadings_text += f"  {name}: {pca.components_[0, j]:+.2f} / {pca.components_[1, j]:+.2f}\n"
    ax.text(
        0.98, 0.02, loadings_text.strip(),
        transform=ax.transAxes, fontsize=8,
        verticalalignment="bottom", horizontalalignment="right",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="wheat", alpha=0.7),
        family="monospace",
    )

    fig.tight_layout()
    outpath = os.path.join(OUTPUT_DIR, "pca_visualization.png")
    fig.savefig(outpath, dpi=150)
    plt.close(fig)
    print(f"Saved {outpath}")


# ===========================================================================
# Visualization 2 — Parallel Coordinates
# ===========================================================================

def plot_parallel_coordinates(points, optimal, c):
    """
    Draw a parallel-coordinates plot where each vertical axis is one of
    the five decision variables.  Lines are coloured by objective value.
    The optimal solution is drawn in bold red.
    """

    n_vars = points.shape[1]
    var_names = ["x₁", "x₂", "x₃", "x₄", "x₅"]
    obj_vals = points @ c

    # Normalise each variable to [0, 1] for visual clarity
    mins = points.min(axis=0)
    maxs = points.max(axis=0)
    ranges = maxs - mins
    ranges[ranges < 1e-9] = 1.0
    normed = (points - mins) / ranges

    opt_normed = (optimal - mins) / ranges

    fig, ax = plt.subplots(figsize=(10, 7))

    # Colour map based on objective value
    norm = plt.Normalize(obj_vals.min(), obj_vals.max())
    cmap = plt.cm.viridis

    xs = np.arange(n_vars)

    # Draw a subset to avoid overplotting (use 200 random lines)
    rng = np.random.default_rng(0)
    idx = rng.choice(len(normed), size=min(200, len(normed)), replace=False)

    for i in idx:
        ax.plot(xs, normed[i], color=cmap(norm(obj_vals[i])), alpha=0.25, lw=0.8)

    # Draw optimal in bold
    ax.plot(xs, opt_normed, color="red", lw=3, marker="o", ms=8,
            label=f"Optimal  z = {c @ optimal:.2f}", zorder=5)

    ax.set_xticks(xs)
    ax.set_xticklabels(var_names, fontsize=12)
    ax.set_ylabel("Normalised value  [0, 1]", fontsize=11)
    ax.set_title("Parallel Coordinates — 5D Feasible Region", fontsize=13)
    ax.legend(fontsize=10, loc="upper right")
    ax.grid(True, axis="x", alpha=0.4)

    # Add original scale annotations at each axis
    for j in range(n_vars):
        ax.text(j, -0.07, f"{mins[j]:.1f}", ha="center", fontsize=8, color="gray",
                transform=ax.get_xaxis_transform())
        ax.text(j, 1.04, f"{maxs[j]:.1f}", ha="center", fontsize=8, color="gray",
                transform=ax.get_xaxis_transform())

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, pad=0.02)
    cbar.set_label("Objective value z", fontsize=10)

    fig.tight_layout()
    outpath = os.path.join(OUTPUT_DIR, "parallel_coordinates.png")
    fig.savefig(outpath, dpi=150)
    plt.close(fig)
    print(f"Saved {outpath}")


# ===========================================================================
# Visualization 3 — Correlation Heatmap
# ===========================================================================

def plot_correlation_heatmap(points):
    """
    Compute and display the correlation matrix between the five decision
    variables over the sampled feasible points.  This reveals which
    variables are constrained together (positive correlation means they
    tend to increase/decrease together within the feasible region).
    """

    var_names = ["x₁", "x₂", "x₃", "x₄", "x₅"]
    corr = np.corrcoef(points, rowvar=False)

    fig, ax = plt.subplots(figsize=(8, 7))

    im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1, aspect="equal")
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Pearson correlation", fontsize=11)

    ax.set_xticks(range(len(var_names)))
    ax.set_yticks(range(len(var_names)))
    ax.set_xticklabels(var_names, fontsize=12)
    ax.set_yticklabels(var_names, fontsize=12)

    # Annotate each cell with the correlation value
    for i in range(len(var_names)):
        for j in range(len(var_names)):
            color = "white" if abs(corr[i, j]) > 0.6 else "black"
            ax.text(j, i, f"{corr[i, j]:.2f}", ha="center", va="center",
                    fontsize=11, color=color, fontweight="bold")

    ax.set_title(
        "Correlation Heatmap — Variable Relationships\nin 5D Feasible Region",
        fontsize=13,
    )

    fig.tight_layout()
    outpath = os.path.join(OUTPUT_DIR, "correlation_heatmap.png")
    fig.savefig(outpath, dpi=150)
    plt.close(fig)
    print(f"Saved {outpath}")


# ===========================================================================
# Optional — Network LP variable distribution (Japneet's long15.mps)
# ===========================================================================

def try_network_lp_viz():
    """
    If Japneet's long15.mps is available, parse it to extract the
    constraint coefficient matrix and visualise the distribution of
    non-zero coefficients per variable (column) as a histogram plus
    a sparsity overview.
    """

    # Try several possible relative paths
    candidates = [
        os.path.join(SCRIPT_DIR, "..", "Japneet", "Japneet", "data", "long15.mps"),
        os.path.join(SCRIPT_DIR, "..", "Japneet", "data", "long15.mps"),
        os.path.join(SCRIPT_DIR, "..", "japneet", "data", "long15.mps"),
    ]

    mps_path = None
    for p in candidates:
        if os.path.exists(p):
            mps_path = os.path.abspath(p)
            break

    if mps_path is None:
        print("\nJapneet's long15.mps not found — skipping network LP viz.")
        return

    print(f"\nReading network LP from {mps_path} ...")

    # Parse a subset of the COLUMNS section to get variable nonzero counts
    # (full parsing would be very slow for 3M lines, so we sample)
    section = None
    var_nnz = {}         # variable name -> count of nonzero entries
    row_count = 0
    col_lines_read = 0
    max_col_lines = 200_000  # read first 200k column lines for speed

    with open(mps_path, "r") as f:
        for line in f:
            stripped = line.strip()
            if stripped in ("ROWS", "COLUMNS", "RHS", "BOUNDS", "RANGES", "ENDATA"):
                section = stripped
                continue

            if section == "ROWS" and stripped:
                row_count += 1

            if section == "COLUMNS" and stripped:
                col_lines_read += 1
                if col_lines_read > max_col_lines:
                    continue
                parts = stripped.split()
                if len(parts) >= 3:
                    var_name = parts[0]
                    # Each line may have 1 or 2 (row, coeff) pairs
                    n_entries = (len(parts) - 1) // 2
                    var_nnz[var_name] = var_nnz.get(var_name, 0) + n_entries

    n_vars = len(var_nnz)
    print(f"  Rows (constraints): {row_count}")
    print(f"  Variables parsed:   {n_vars}")

    if n_vars == 0:
        print("  No variable data parsed — skipping network viz.")
        return

    counts = np.array(list(var_nnz.values()))

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Left: histogram of non-zeros per variable
    ax1 = axes[0]
    ax1.hist(counts, bins=40, color="steelblue", edgecolor="white", alpha=0.85)
    ax1.set_xlabel("Non-zero entries per variable", fontsize=11)
    ax1.set_ylabel("Number of variables", fontsize=11)
    ax1.set_title("Network LP — Variable Density Distribution", fontsize=12)
    ax1.axvline(counts.mean(), color="red", ls="--", lw=1.5,
                label=f"Mean = {counts.mean():.1f}")
    ax1.axvline(np.median(counts), color="orange", ls="--", lw=1.5,
                label=f"Median = {np.median(counts):.1f}")
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Right: sorted variable density profile
    ax2 = axes[1]
    sorted_counts = np.sort(counts)[::-1]
    ax2.plot(sorted_counts, color="darkorange", lw=1.2)
    ax2.fill_between(range(len(sorted_counts)), sorted_counts,
                     alpha=0.2, color="darkorange")
    ax2.set_xlabel("Variable index (sorted by density)", fontsize=11)
    ax2.set_ylabel("Non-zero entries", fontsize=11)
    ax2.set_title("Network LP — Sparsity Profile", fontsize=12)
    ax2.grid(True, alpha=0.3)

    stats_text = (
        f"Variables: {n_vars}\n"
        f"Constraints: {row_count}\n"
        f"Min nnz: {counts.min()}\n"
        f"Max nnz: {counts.max()}\n"
        f"Mean nnz: {counts.mean():.1f}"
    )
    ax2.text(
        0.97, 0.95, stats_text,
        transform=ax2.transAxes, fontsize=9,
        verticalalignment="top", horizontalalignment="right",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="lightyellow", alpha=0.8),
        family="monospace",
    )

    fig.suptitle(
        "Mittelmann Network-LP Benchmark — long15.mps",
        fontsize=14, fontweight="bold", y=1.01,
    )
    fig.tight_layout()
    outpath = os.path.join(OUTPUT_DIR, "network_variable_distribution.png")
    fig.savefig(outpath, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {outpath}")


# ===========================================================================
# Main
# ===========================================================================

def main():
    ensure_output_dir()

    # Step 1 — Build and solve the higher-dim LP
    A, b, c, optimal = build_higher_dim_lp()

    # Step 2 — Sample feasible points for scatter-based visualizations
    points = sample_feasible_points(A, b, n_samples=500)

    if len(points) < 20:
        print("Error: not enough feasible points sampled. Check LP constraints.")
        sys.exit(1)

    # Step 3 — Generate the three required visualizations
    plot_pca(points, optimal, A, b, c)
    plot_parallel_coordinates(points, optimal, c)
    plot_correlation_heatmap(points)

    # Step 4 — Optional: Japneet's network LP visualization
    try_network_lp_viz()

    print("\n" + "=" * 55)
    print("All higher-dimensional visualizations complete.")
    print("=" * 55)


if __name__ == "__main__":
    main()
