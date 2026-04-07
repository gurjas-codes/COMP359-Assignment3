"""
Library-based LP Solver with 5+ constraints
Uses PuLP library
"""

import pulp
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import warnings
warnings.filterwarnings('ignore')

# Add parent directory to path to import Bryan's module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Bryan.constraints import plot_line, plot_vertical_line, plot_horizontal_line

def solve_lp():
    """
    Problem: Maximize Z = 4x + 3y
    Constraints (7 total):
    1. x + y <= 8
    2. 2x + y <= 12
    3. x + 2y <= 10
    4. x >= 1
    5. y >= 1
    6. x <= 6
    7. y <= 5
    """
    
    # Create problem
    prob = pulp.LpProblem("Linear_Programming_Problem", pulp.LpMaximize)
    
    # Variables
    x = pulp.LpVariable("x", lowBound=0)
    y = pulp.LpVariable("y", lowBound=0)
    
    # Objective
    prob += 4*x + 3*y, "Objective"
    
    # Constraints (7 total)
    prob += x + y <= 8, "constraint_1"
    prob += 2*x + y <= 12, "constraint_2"
    prob += x + 2*y <= 10, "constraint_3"
    prob += x >= 1, "constraint_4"
    prob += y >= 1, "constraint_5"
    prob += x <= 6, "constraint_6"
    prob += y <= 5, "constraint_7"
    
    # Solve (silent mode)
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    # Results
    result = {
        'status': pulp.LpStatus[prob.status],
        'x': pulp.value(x),
        'y': pulp.value(y),
        'objective': pulp.value(prob.objective),
        'constraints': {}
    }
    
    # Record constraint slack
    for name, constraint in prob.constraints.items():
        result['constraints'][name] = pulp.value(constraint)
    
    return result, prob

def visualize_solution(result):
    """Plot feasible region and solution point"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Plot each constraint line
    x_range = [0, 7]
    
    # Main constraints
    plot_line(ax, x_range, -1, 8, 'x + y = 8', linestyle='--', alpha=0.7, color='red')
    plot_line(ax, x_range, -2, 12, '2x + y = 12', linestyle='--', alpha=0.7, color='blue')
    plot_line(ax, x_range, -0.5, 5, 'x + 2y = 10', linestyle='--', alpha=0.7, color='green')
    
    # Bounds
    plot_vertical_line(ax, 1, 'x = 1')
    plot_vertical_line(ax, 6, 'x = 6')
    plot_horizontal_line(ax, 1, 'y = 1')
    plot_horizontal_line(ax, 5, 'y = 5')
    
    # Find feasible region by sampling
    x_vals = np.linspace(0, 7, 200)
    y_vals = np.linspace(0, 6, 200)
    X, Y = np.meshgrid(x_vals, y_vals)
    
    # Check all constraints
    feasible = (X + Y <= 8) & (2*X + Y <= 12) & (X + 2*Y <= 10) & (X >= 1) & (Y >= 1) & (X <= 6) & (Y <= 5)
    
    # Plot feasible region
    ax.contourf(X, Y, feasible, levels=[0.5, 1], colors=['lightgreen'], alpha=0.5)
    
    # Plot solution point
    ax.plot(result['x'], result['y'], 'ro', markersize=12, label=f"Optimal: ({result['x']:.2f}, {result['y']:.2f})")
    ax.annotate(f"Z = {result['objective']:.2f}", 
                (result['x'] + 0.2, result['y'] + 0.2), 
                fontsize=12, fontweight='bold')
    
    # Formatting
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 6)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'LP Solution: {result["status"]}\nMax Z = 4x + 3y = {result["objective"]:.2f}')
    ax.legend(loc='upper right', fontsize=8, ncol=2)
    ax.grid(True, alpha=0.3)
    
    # Save plot
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, 'solution_plot.png')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    
    return fig, ax

if __name__ == "__main__":
    result, prob = solve_lp()
    visualize_solution(result)