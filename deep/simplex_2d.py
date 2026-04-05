from __future__ import annotations

from pathlib import Path

import numpy as np

import plot_all
from simplex_2d import LinearProgram, plot_step, solve_simplex_with_trace


MAX_INEQUALITIES = 8


def prompt_int(prompt: str, minimum: int, maximum: int) -> int:
    """Read an integer inside a closed interval."""

    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if minimum <= value <= maximum:
            return value
        print(f"Please enter a value from {minimum} to {maximum}.")


def prompt_float(prompt: str) -> float:
    """Read a floating-point number."""

    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print("Please enter a valid number.")


def read_linear_program() -> LinearProgram:
    """Collect a 2D maximization problem in standard <= form from the user."""

    # Keep the script narrowly focused on 2D input so the plotting logic stays simple.
    print("2D simplex solver")
    print("Variables are fixed as x and y.")
    print("Enter each inequality in the form: ax + by <= c")
    print("x >= 0 and y >= 0 are included automatically.")
    print()

    constraint_count = prompt_int(
        f"How many inequalities do you want to enter? (1-{MAX_INEQUALITIES}): ",
        1,
        MAX_INEQUALITIES,
    )

    print()
    print("Objective function: maximize z = p*x + q*y")
    objective_x = prompt_float("Enter coefficient p for x: ")
    objective_y = prompt_float("Enter coefficient q for y: ")

    rows = []
    rhs_values = []

    # Store the inequalities as A x <= b so the simplex helper can use them directly.
    for index in range(constraint_count):
        print()
        print(f"Inequality {index + 1}: a*x + b*y <= c")
        a_coeff = prompt_float("Coefficient a for x: ")
        b_coeff = prompt_float("Coefficient b for y: ")
        rhs = prompt_float("Right-hand side c: ")
        if rhs < 0:
            raise ValueError(
                "This program requires each right-hand side c to be non-negative."
            )
        rows.append([a_coeff, b_coeff])
        rhs_values.append(rhs)

    return LinearProgram(
        # Package the user's values into the solver's A, b, c representation.
        A=np.array(rows, dtype=float),
        b=np.array(rhs_values, dtype=float),
        c=np.array([objective_x, objective_y], dtype=float),
    )


def clear_old_outputs(out_dir: Path) -> None:
    """Remove old simplex images so the combined plot only uses the current run."""

    for image_path in out_dir.glob("simplex_2d_step_*.png"):
        try:
            image_path.unlink(missing_ok=True)
        except PermissionError:
            # Ignore locked files and continue generating the current run's images.
            pass
    try:
        (out_dir / "simplex_2d_all.png").unlink(missing_ok=True)
    except PermissionError:
        pass


def format_objective(lp: LinearProgram, point: tuple[float, float]) -> float:
    """Evaluate z = c^T x at a point."""

    return float(lp.c[0] * point[0] + lp.c[1] * point[1])


def main() -> None:
    try:
        # Read the LP from the terminal, then ask the simplex helper for the BFS trace.
        lp = read_linear_program()
        trace = solve_simplex_with_trace(lp)
    except ValueError as exc:
        print(f"Input error: {exc}")
        return

    out_dir = Path(__file__).resolve().parent
    clear_old_outputs(out_dir)
    current_images = []

    # Save one image for each visited basic feasible solution.
    for step_index in range(len(trace)):
        partial_path = trace[: step_index + 1]
        if step_index == 0:
            title = "initial BFS"
        elif step_index == len(trace) - 1:
            title = "optimal vertex"
        else:
            title = f"pivot {step_index}"

        outfile = out_dir / f"simplex_2d_step_{step_index + 1}.png"
        plot_step(lp, partial_path, step_index, title, str(outfile))
        current_images.append(outfile)
        print(f"Wrote {outfile}")

    # Combine the per-step images into one summary figure.
    plot_all.combine_images(current_images, out_dir / "simplex_2d_all.png")

    best_point = trace[-1]
    # The last recorded BFS is the optimum once simplex stops improving.
    best_value = format_objective(lp, best_point)

    print()
    print("Simplex path:")
    for index, (x_value, y_value) in enumerate(trace):
        # Print the same order used in the saved plots so the text and images match.
        print(f"Step {index}: x = {x_value:.4f}, y = {y_value:.4f}")

    print()
    print(f"Optimal solution: x = {best_point[0]:.4f}, y = {best_point[1]:.4f}")
    print(f"Maximum objective value: z = {best_value:.4f}")
    print(f"Combined plot: {out_dir / 'simplex_2d_all.png'}")


if __name__ == "__main__":
    main()
