"""
Jovan - Library Solver (PuLP)

This file solves a linear programming problem using the PuLP library.
We are maximizing Z = 4x + 3y with 7 constraints.

This shows how we can solve LP problems using code instead of doing
everything manually (like with the Simplex method).
"""

import os
import pulp
import numpy as np
import matplotlib.pyplot as plt


def solve_lp():
    """
    Builds and solves the LP using PuLP.

    Returns:
        result (dict): contains solution values, objective, and constraint info
        prob (LpProblem): the full LP model (useful if needed later)
    """

    # Create the LP problem (Maximization)
    prob = pulp.LpProblem("Linear_Programming_Problem", pulp.LpMaximize)

    # Decision variables
    # lowBound=0 means x and y cannot be negative
    x = pulp.LpVariable("x", lowBound=0)
    y = pulp.LpVariable("y", lowBound=0)

    # Objective function
    # This is what we are trying to maximize
    prob += 4 * x + 3 * y, "Objective"

    # Constraints (7 total)
    # These define the feasible region
    prob += x + y <= 8, "c1_x_plus_y_le_8"
    prob += 2 * x + y <= 12, "c2_2x_plus_y_le_12"
    prob += x + 2 * y <= 10, "c3_x_plus_2y_le_10"
    prob += x >= 1, "c4_x_ge_1"
    prob += y >= 1, "c5_y_ge_1"
    prob += x <= 6, "c6_x_le_6"
    prob += y <= 5, "c7_y_le_5"

    # Solve the problem using CBC solver (default in PuLP)
    # msg=False just hides solver logs so output is cleaner
    solver = pulp.PULP_CBC_CMD(msg=False)
    prob.solve(solver)

    # Extract solution values
    x_val = pulp.value(x)
    y_val = pulp.value(y)
    obj_val = pulp.value(prob.objective)

    # Manually compute slack/surplus values
    # This helps us understand which constraints are "tight" (binding)
    constraints_info = {
        "c1_x_plus_y_le_8": {"lhs": x_val + y_val, "rhs": 8, "type": "<="},
        "c2_2x_plus_y_le_12": {"lhs": 2 * x_val + y_val, "rhs": 12, "type": "<="},
        "c3_x_plus_2y_le_10": {"lhs": x_val + 2 * y_val, "rhs": 10, "type": "<="},
        "c4_x_ge_1": {"lhs": x_val, "rhs": 1, "type": ">="},
        "c5_y_ge_1": {"lhs": y_val, "rhs": 1, "type": ">="},
        "c6_x_le_6": {"lhs": x_val, "rhs": 6, "type": "<="},
        "c7_y_le_5": {"lhs": y_val, "rhs": 5, "type": "<="},
    }

    # Calculate slack/surplus and check if constraint is binding
    for name, info in constraints_info.items():
        if info["type"] == "<=":
            info["slack"] = info["rhs"] - info["lhs"]
        else:
            info["slack"] = info["lhs"] - info["rhs"]

        # If slack is ~0, constraint is active (binding)
        info["binding"] = abs(info["slack"]) < 1e-6

    result = {
        "status": pulp.LpStatus[prob.status],
        "x": x_val,
        "y": y_val,
        "objective": obj_val,
        "constraints": constraints_info,
    }

    return result, prob


def plot_constraint_line(ax, x_vals, a, b, c, label):
    """
    Plots a constraint line of the form:
        a*x + b*y = c

    This is used just for visualization (not solving).
    """

    # If b = 0, this is a vertical line (x = constant)
    if abs(b) < 1e-12:
        x_line = c / a
        ax.axvline(x=x_line, linestyle="--", linewidth=1.5, label=label)
    else:
        # Rearranged to y = (c - ax)/b
        y_vals = (c - a * x_vals) / b
        ax.plot(x_vals, y_vals, linestyle="--", linewidth=1.5, label=label)


def visualize_solution(result, output_path="Jovan/solution_plot.png"):
    """
    Plots:
    - all constraint lines
    - feasible region (shaded)
    - optimal solution point
    """

    fig, ax = plt.subplots(figsize=(10, 8))

    # Create grid of points to test feasibility
    x_vals = np.linspace(0, 7, 500)
    y_vals = np.linspace(0, 6, 500)
    X, Y = np.meshgrid(x_vals, y_vals)

    # Check which points satisfy ALL constraints
    feasible = (
        (X + Y <= 8) &
        (2 * X + Y <= 12) &
        (X + 2 * Y <= 10) &
        (X >= 1) &
        (Y >= 1) &
        (X <= 6) &
        (Y <= 5)
    )

    # Shade feasible region
    ax.contourf(X, Y, feasible, levels=[0.5, 1], alpha=0.35)

    # Plot each constraint boundary
    plot_constraint_line(ax, x_vals, 1, 1, 8, "x + y = 8")
    plot_constraint_line(ax, x_vals, 2, 1, 12, "2x + y = 12")
    plot_constraint_line(ax, x_vals, 1, 2, 10, "x + 2y = 10")
    plot_constraint_line(ax, x_vals, 1, 0, 1, "x = 1")
    plot_constraint_line(ax, x_vals, 0, 1, 1, "y = 1")
    plot_constraint_line(ax, x_vals, 1, 0, 6, "x = 6")
    plot_constraint_line(ax, x_vals, 0, 1, 5, "y = 5")

    # Plot optimal point
    ax.plot(result["x"], result["y"], "ro", markersize=10,
            label=f'Optimal ({result["x"]:.2f}, {result["y"]:.2f})')

    # Label objective value near the point
    ax.annotate(
        f'Z = {result["objective"]:.2f}',
        (result["x"], result["y"]),
        xytext=(result["x"] + 0.25, result["y"] + 0.25),
        arrowprops=dict(arrowstyle="->"),
        fontsize=11,
        fontweight="bold"
    )

    # Formatting
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 6)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f'Max Z = 4x + 3y = {result["objective"]:.2f}')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8, loc="upper right", ncol=2)

    plt.tight_layout()

    # Save plot
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    print(f"Saved plot to: {output_path}")

    return fig, ax


def print_results(result):
    """
    Prints solution in a readable way.
    Also shows which constraints are binding.
    """

    print("\n" + "=" * 60)
    print("LP SOLVER RESULTS")
    print("=" * 60)

    print(f"Status: {result['status']}")
    print(f"x = {result['x']:.4f}")
    print(f"y = {result['y']:.4f}")
    print(f"Max Z = {result['objective']:.4f}")

    print("\nConstraint analysis:")
    for name, info in result["constraints"].items():
        binding_text = "binding" if info["binding"] else "not binding"

        print(
            f"  {name}: "
            f"LHS={info['lhs']:.4f}, RHS={info['rhs']:.4f}, "
            f"slack={info['slack']:.4f} ({binding_text})"
        )


if __name__ == "__main__":
    # Required libraries:
    # pip install pulp numpy matplotlib

    result, prob = solve_lp()

    print_results(result)

    # Generate visualization
    visualize_solution(result)


    