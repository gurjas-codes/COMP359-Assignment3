"""
Combined plot showing all simplex steps
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

def main():
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create figure with 1x3 subplots
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Load and display each step
    for i in range(3):
        img_path = os.path.join(script_dir, f'simplex_2d_step_{i+1}.png')
        if os.path.exists(img_path):
            img = mpimg.imread(img_path)
            axes[i].imshow(img)
            axes[i].axis('off')
            axes[i].set_title(f'Step {i+1}', fontsize=14)
        else:
            axes[i].text(0.5, 0.5, f'Step {i+1}\n(not found)', 
                        ha='center', va='center', transform=axes[i].transAxes)
            axes[i].axis('off')
    
    plt.suptitle('Simplex Algorithm Steps - 2D Visualization', fontsize=16)
    plt.tight_layout()
    
    # Save combined image
    output_path = os.path.join(script_dir, 'simplex_2d_all.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Saved combined plot: {output_path}")
    plt.close()

if __name__ == "__main__":
    main()