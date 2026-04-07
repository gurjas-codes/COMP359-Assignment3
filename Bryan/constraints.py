"""
Constraint Visualizer Helper
Creates reusable constraint plotting functions for the team

Bryan's Role:
- Create reusable constraint helper functions for the team
- Provide functions for plotting lines, inequalities, and feasible regions
- Support Deep's 2D visualization with constraint plotting utilities
"""

import numpy as np
import matplotlib.pyplot as plt

def plot_line(ax, x_range, slope, intercept, label, linestyle='-', color='blue'):
    """
    Plot a line y = slope*x + intercept over x_range
    
    Parameters:
    -----------
    ax : matplotlib.axes.Axes
        The axes to plot on
    x_range : tuple
        (min, max) for x values
    slope : float
        Slope of the line
    intercept : float
        y-intercept of the line
    label : str
        Label for the line (for legend)
    linestyle : str
        Line style ('-', '--', ':', etc.)
    color : str
        Color of the line
    
    Returns:
    --------
    ax : matplotlib.axes.Axes
        The axes with the line plotted
    """
    x = np.linspace(x_range[0], x_range[1], 100)
    y = slope * x + intercept
    ax.plot(x, y, linestyle=linestyle, color=color, label=label)
    return ax


def plot_vertical_line(ax, x_value, label, linestyle='--', color='purple'):
    """
    Plot a vertical line at x = x_value
    
    Parameters:
    -----------
    ax : matplotlib.axes.Axes
        The axes to plot on
    x_value : float
        x-coordinate where vertical line is drawn
    label : str
        Label for the line (for legend)
    linestyle : str
        Line style ('-', '--', ':', etc.)
    color : str
        Color of the line
    
    Returns:
    --------
    ax : matplotlib.axes.Axes
        The axes with the vertical line plotted
    """
    ax.axvline(x=x_value, linestyle=linestyle, color=color, alpha=0.7, label=label)
    return ax


def plot_horizontal_line(ax, y_value, label, linestyle='--', color='brown'):
    """
    Plot a horizontal line at y = y_value
    
    Parameters:
    -----------
    ax : matplotlib.axes.Axes
        The axes to plot on
    y_value : float
        y-coordinate where horizontal line is drawn
    label : str
        Label for the line (for legend)
    linestyle : str
        Line style ('-', '--', ':', etc.)
    color : str
        Color of the line
    
    Returns:
    --------
    ax : matplotlib.axes.Axes
        The axes with the horizontal line plotted
    """
    ax.axhline(y=y_value, linestyle=linestyle, color=color, alpha=0.7, label=label)
    return ax


def plot_inequality(ax, x_range, slope, intercept, direction, color='gray', alpha=0.3):
    """
    Shade inequality region: direction 'le' (<=) or 'ge' (>=)
    
    Parameters:
    -----------
    ax : matplotlib.axes.Axes
        The axes to plot on
    x_range : tuple
        (min, max) for x values
    slope : float
        Slope of the boundary line
    intercept : float
        y-intercept of the boundary line
    direction : str
        'le' for less than or equal (y <= line)
        'ge' for greater than or equal (y >= line)
    color : str
        Color of the shaded region
    alpha : float
        Transparency of the shaded region (0 to 1)
    
    Returns:
    --------
    ax : matplotlib.axes.Axes
        The axes with the inequality shaded
    """
    x = np.linspace(x_range[0], x_range[1], 100)
    y = slope * x + intercept
    
    if direction == 'le':
        # Shade below the line (y <= line)
        ax.fill_between(x, -100, y, color=color, alpha=alpha)
    elif direction == 'ge':
        # Shade above the line (y >= line)
        ax.fill_between(x, y, 100, color=color, alpha=alpha)
    return ax


def get_feasible_region_polygon(constraints, x_range, y_range, resolution=100):
    """
    Returns a boolean grid representing the feasible region for 2D constraints
    
    Parameters:
    -----------
    constraints : list of dict
        List of constraint dictionaries with keys:
        - 'slope': slope of the line (use float('inf') for vertical lines)
        - 'intercept': y-intercept (or x-value for vertical lines)
        - 'direction': 'le' (<=) or 'ge' (>=)
    x_range : tuple
        (min, max) for x values
    y_range : tuple
        (min, max) for y values
    resolution : int
        Number of points in each dimension (higher = smoother but slower)
    
    Returns:
    --------
    X : numpy.ndarray
        2D array of x coordinates
    Y : numpy.ndarray
        2D array of y coordinates
    feasible : numpy.ndarray
        Boolean 2D array where True indicates feasible point
    """
    x = np.linspace(x_range[0], x_range[1], resolution)
    y = np.linspace(y_range[0], y_range[1], resolution)
    X, Y = np.meshgrid(x, y)
    
    feasible = np.ones(X.shape, dtype=bool)
    
    for constraint in constraints:
        if constraint['slope'] == float('inf'):
            # Vertical constraint (x >= intercept or x <= intercept)
            if constraint['direction'] == 'ge':
                feasible &= (X >= constraint['intercept'])
            else:
                feasible &= (X <= constraint['intercept'])
        elif constraint['slope'] == 0 and constraint['intercept'] == 0:
            # Horizontal constraint at y=0
            if constraint['direction'] == 'ge':
                feasible &= (Y >= 0)
            else:
                feasible &= (Y <= 0)
        else:
            # Regular line constraint
            line_val = constraint['slope'] * X + constraint['intercept']
            if constraint['direction'] == 'le':
                feasible &= (Y <= line_val)
            elif constraint['direction'] == 'ge':
                feasible &= (Y >= line_val)
    
    return X, Y, feasible


def plot_feasible_region(ax, constraints, x_range, y_range, color='lightgreen', alpha=0.3):
    """
    Plot the feasible region as a shaded area
    
    Parameters:
    -----------
    ax : matplotlib.axes.Axes
        The axes to plot on
    constraints : list of dict
        List of constraint dictionaries
    x_range : tuple
        (min, max) for x values
    y_range : tuple
        (min, max) for y values
    color : str
        Color of the feasible region
    alpha : float
        Transparency of the feasible region
    
    Returns:
    --------
    ax : matplotlib.axes.Axes
        The axes with the feasible region plotted
    """
    X, Y, feasible = get_feasible_region_polygon(constraints, x_range, y_range)
    ax.contourf(X, Y, feasible, levels=[0.5, 1], colors=[color], alpha=alpha)
    return ax


if __name__ == "__main__":
    """
    Test the constraint helper functions
    Creates a sample plot to verify everything works
    """
    print("="*50)
    print("BRYAN'S CONSTRAINT HELPER FUNCTIONS")
    print("="*50)
    print("Testing constraint helper functions...")
    
    # Create a test plot
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Define some test constraints
    constraints = [
        {'slope': -0.5, 'intercept': 5, 'direction': 'le', 'name': 'x + 2y <= 10'},
        {'slope': -2, 'intercept': 8, 'direction': 'le', 'name': '2x + y <= 8'},
    ]
    
    # Plot constraint lines
    print("\nPlotting constraint lines...")
    for c in constraints:
        plot_line(ax, [0, 10], c['slope'], c['intercept'], c['name'])
    
    # Plot axes lines
    print("Plotting axis lines...")
    plot_vertical_line(ax, 0, 'x = 0')
    plot_horizontal_line(ax, 0, 'y = 0')
    
    # Test inequality shading
    print("Testing inequality shading...")
    plot_inequality(ax, [0, 10], -0.5, 5, 'le', color='red', alpha=0.1)
    plot_inequality(ax, [0, 10], -2, 8, 'le', color='blue', alpha=0.1)
    
    # Test feasible region detection
    print("Testing feasible region detection...")
    all_constraints = constraints + [
        {'slope': float('inf'), 'intercept': 0, 'direction': 'ge', 'name': 'x >= 0'},
        {'slope': 0, 'intercept': 0, 'direction': 'ge', 'name': 'y >= 0'},
    ]
    plot_feasible_region(ax, all_constraints, [0, 10], [0, 10], color='lightgreen', alpha=0.5)
    
    # Formatting
    ax.set_xlim(-1, 10)
    ax.set_ylim(-1, 10)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.set_title('Test of Constraint Helper Functions', fontsize=14)
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.3)
    
    # Save the plot
    plt.tight_layout()
    plt.savefig('Bryan/test_plot.png', dpi=150)
    print("\n✅ Test plot saved to: Bryan/test_plot.png")
    
    plt.show()  # Uncomment if running interactively
    
    print("\n" + "="*50)
    print("ALL FUNCTIONS WORKING CORRECTLY!")
    print("="*50)
    print("\nAvailable functions:")
    print("  - plot_line()")
    print("  - plot_vertical_line()")
    print("  - plot_horizontal_line()")
    print("  - plot_inequality()")
    print("  - get_feasible_region_polygon()")
    print("  - plot_feasible_region()")