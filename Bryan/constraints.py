
"""
Constraint Visualizer Helper
Creates reusable constraint plotting functions for the team
"""

import numpy as np
import matplotlib.pyplot as plt
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def plot_line(ax, x_range, slope, intercept, label, linestyle='-', color='blue'):
    """Plot a line y = slope*x + intercept over x_range"""
    x = np.linspace(x_range[0], x_range[1], 100)
    y = slope * x + intercept
    ax.plot(x, y, linestyle=linestyle, color=color, label=label)
    return ax

def plot_vertical_line(ax, x_value, label, linestyle='--', color='purple'):
    """Plots a vertical line at x = x_value"""
    ax.axvline(x=x_value, linestyle=linestyle, color=color, label=label)
    return ax

def plot_horizontal_line(ax, y_value, label, linestyle='--', color='brown'):
    """Plots a horizontal line at y = y_value"""
    ax.axhline(y=y_value, linestyle=linestyle, color=color, label=label)
    return ax
    

def plot_inequality(ax, x_range, slope, intercept, direction, color='gray', alpha=0.3):
    """Shade inequality region: direction 'le' (<=) or 'ge' (>=)"""
    x = np.linspace(x_range[0], x_range[1], 100)
    y = slope * x + intercept
    
    if direction == 'le':
        ax.fill_between(x, -100, y, color=color, alpha=alpha)
    elif direction == 'ge':
        ax.fill_between(x, y, 100, color=color, alpha=alpha)
    return ax

def get_feasible_region_polygon(constraints, x_range, y_range, resolution=100):
    """
    Returns a polygon of the feasible region for 2D constraints
    constraints: list of dicts with {'slope', 'intercept', 'direction', 'x_range'}
    """
    x = np.linspace(x_range[0], x_range[1], resolution)
    y = np.linspace(y_range[0], y_range[1], resolution)
    X, Y = np.meshgrid(x, y)
    
    feasible = np.ones(X.shape, dtype=bool)
    
    for constraint in constraints:
        line_val = constraint['slope'] * X + constraint['intercept']
        if constraint['direction'] == 'le':
            feasible &= (Y <= line_val)
        elif constraint['direction'] == 'ge':
            feasible &= (Y >= line_val)
    
    return X, Y, feasible

if __name__ == "__main__":
    # Test the functions
    print("Constraint helper functions loaded successfully!")
    
    # Example test plot
    fig, ax = plt.subplots(figsize=(8, 6))
    plot_vertical_line(ax, x_value=1, label='x = 1', linestyle='--', color='purple')
    plot_horizontal_line(ax, y_value=1, label='y = 1', linestyle='--', color='brown')
    
    constraints = [
        {'slope': -0.5, 'intercept': 5, 'direction': 'le', 'name': 'x + 2y <= 10'},
        {'slope': -2, 'intercept': 8, 'direction': 'le', 'name': '2x + y <= 8'},
        {'slope': 0, 'intercept': 0, 'direction': 'ge', 'name': 'y >= 0'},
    ]
    
    for c in constraints:
        plot_line(ax, [0, 10], c['slope'], c['intercept'], c['name'])
    
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Test Constraint Plot')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.savefig(os.path.join(SCRIPT_DIR, 'test_plot.png'))
    print("Test plot saved to bryan/test_plot.png")
    plt.show()  # Uncomment if running interactively
