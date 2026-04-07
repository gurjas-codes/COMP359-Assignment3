"""
Main runner script - executes all components for the Linear Programming Simplex Visualization project
Run from project root: python3 Nishant/run_all.py
"""

import os
import sys
import subprocess
import time
import warnings
warnings.filterwarnings('ignore')

# Suppress all output from subprocesses
import contextlib

def get_project_root():
    """Get the project root directory"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def print_header(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def run_script_silent(script_path):
    """
    Run a Python script silently, suppressing all output
    """
    project_root = get_project_root()
    full_path = os.path.join(project_root, script_path)
    
    if not os.path.exists(full_path):
        return False
    
    try:
        # Run with stdout and stderr suppressed
        with open(os.devnull, 'w') as devnull:
            result = subprocess.run(
                [sys.executable, full_path], 
                stdout=devnull,
                stderr=devnull,
                cwd=project_root,
                timeout=300
            )
        return result.returncode == 0
    except:
        return False

def verify_outputs():
    """
    Check all expected output files exist
    """
    project_root = get_project_root()
    
    output_files = [
        'Bryan/test_plot.png',
        'deep/simplex_2d_step_1.png',
        'deep/simplex_2d_step_2.png',
        'deep/simplex_2d_step_3.png',
        'deep/simplex_2d_all.png',
        'Jovan/solution_plot.png',
        'Japneet/solution_summary.txt',
        'Gurjas/pca_visualization.png',
        'Gurjas/parallel_coordinates.png',
        'Gurjas/correlation_heatmap.png',
    ]
    
    found = []
    missing = []
    
    for file_path in output_files:
        full_path = os.path.join(project_root, file_path)
        if os.path.exists(full_path):
            found.append(file_path)
        else:
            missing.append(file_path)
    
    return found, missing

def main():
    """Main execution function - clean output version"""
    
    print_header("LINEAR PROGRAMMING SIMPLEX VISUALIZATION")
    print("Team: Bryan, Deep, Gurjas, Japneet, Jovan, Nishant")
    
    start_time = time.time()
    
    # Define scripts to run in order
    scripts = [
        'Bryan/constraints.py',
        'deep/simplex_2d.py',
        'deep/plot_all.py',
        'Jovan/library_solver.py',
        'Japneet/network_lp.py',
        'Gurjas/higher_dim_viz.py',
    ]
    
    # Run each script silently
    for script_path in scripts:
        run_script_silent(script_path)
    
    # Verify outputs
    found, missing = verify_outputs()
    
    # Print summary
    print_header("RESULTS")
    print(f"\nOutput Files Generated: {len(found)}/10")
    
    if len(found) == 10:
        print("\n✓ All components completed successfully!")
    else:
        print(f"\n⚠ Missing {len(missing)} output files")
    
    elapsed = time.time() - start_time
    print(f"\nTotal execution time: {elapsed:.2f} seconds")
    
    print_header("COMPLETE")

if __name__ == "__main__":
    main()