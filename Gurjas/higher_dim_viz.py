"""
Higher-dimensional visualization techniques
Attempts to visualize high-dimensional LP solutions in 2D
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import sys
import os
import warnings
warnings.filterwarnings('ignore')

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def generate_synthetic_highdim_data(n_dimensions=50, n_points=100):
    """
    Generate synthetic high-dimensional LP-like data
    Simulates solution vectors from a high-dimensional LP
    """
    np.random.seed(42)
    
    # Simulate optimal solution vectors
    solutions = []
    for _ in range(n_points):
        solution = np.random.rand(n_dimensions)
        solution = solution / solution.sum()  # Normalize to sum to 1
        solutions.append(solution)
    
    solutions = np.array(solutions)
    
    # Add objective values (higher is better)
    objectives = np.random.rand(n_points) * 100
    
    return solutions, objectives

def pca_visualization(data, objectives, output_path):
    """Apply PCA to reduce to 2D and plot"""
    
    # Standardize
    data_scaled = (data - data.mean(axis=0)) / data.std(axis=0)
    
    # PCA
    pca = PCA(n_components=2)
    data_2d = pca.fit_transform(data_scaled)
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 8))
    
    scatter = ax.scatter(data_2d[:, 0], data_2d[:, 1], 
                        c=objectives, cmap='viridis', 
                        s=50, alpha=0.7)
    
    ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)')
    ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)')
    ax.set_title('PCA Visualization of High-Dimensional LP Solutions\nColored by Objective Value')
    ax.grid(True, alpha=0.3)
    
    cbar = plt.colorbar(scatter, ax=ax, label='Objective Value')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    
    return fig, ax

def parallel_coordinates(data, objectives, output_path, n_dimensions_to_show=10):
    """Create parallel coordinates plot for high-dimensional data"""
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Normalize data for plotting
    data_norm = (data - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0) + 1e-10)
    
    # Only show first n_dimensions_to_show for readability
    data_subset = data_norm[:, :n_dimensions_to_show]
    
    # Create parallel coordinates
    x_ticks = range(n_dimensions_to_show)
    
    # Color by objective (normalized for colormap)
    obj_norm = (objectives - objectives.min()) / (objectives.max() - objectives.min() + 1e-10)
    
    for i in range(min(len(data_subset), 50)):  # Limit to 50 lines for readability
        ax.plot(x_ticks, data_subset[i], 'o-', 
                color=plt.cm.viridis(obj_norm[i]), 
                alpha=0.5, linewidth=1, markersize=3)
    
    ax.set_xlabel('Dimension Index')
    ax.set_ylabel('Normalized Value')
    ax.set_title(f'Parallel Coordinates Plot (first {n_dimensions_to_show} dimensions)\nColored by Objective Value')
    ax.set_xticks(x_ticks)
    
    # Add colorbar - FIXED: explicitly specify ax
    sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(objectives.min(), objectives.max()))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, label='Objective Value')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    
    return fig, ax

def heatmap_visualization(data, output_path):
    """Create heatmap showing relationships between dimensions"""
    
    # Calculate correlation matrix (limit to 30 dimensions for readability)
    data_subset = data[:, :min(30, data.shape[1])]
    corr_matrix = np.corrcoef(data_subset.T)
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    im = ax.imshow(corr_matrix, cmap='RdBu_r', vmin=-1, vmax=1)
    
    ax.set_xlabel('Dimension')
    ax.set_ylabel('Dimension')
    ax.set_title('Correlation Heatmap of High-Dimensional Solution Space')
    
    cbar = plt.colorbar(im, ax=ax, label='Correlation Coefficient')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    
    return fig, ax

def create_distribution_plot(data, output_path):
    """Create distribution plot of variable values"""
    
    # Flatten data or take first dimension
    values = data.flatten()[:1000]  # Limit for performance
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(values, bins=50, alpha=0.7, color='steelblue', edgecolor='black')
    ax.set_xlabel('Variable Value')
    ax.set_ylabel('Frequency')
    ax.set_title('Distribution of Variable Values in High-Dimensional LP')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

def main():
    """Main execution function - silent mode"""
    
    # Get output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Generate synthetic high-dimensional data
    data, objectives = generate_synthetic_highdim_data()
    
    # Create visualizations
    pca_visualization(data, objectives, os.path.join(script_dir, 'pca_visualization.png'))
    parallel_coordinates(data, objectives, os.path.join(script_dir, 'parallel_coordinates.png'))
    heatmap_visualization(data, os.path.join(script_dir, 'correlation_heatmap.png'))
    create_distribution_plot(data, os.path.join(script_dir, 'network_variable_distribution.png'))

if __name__ == "__main__":
    main()