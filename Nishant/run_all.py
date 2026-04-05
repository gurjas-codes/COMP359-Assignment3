"""

This script coordinates execution of all team members' code:
- Bryan: constraint helper functions
- Deep: 2D simplex visualization
- Jovan: library solver with 5+ constraints
- Japneet: network LP (long15.mps) solver
- Gurjas: higher-dimensional visualization

run from project root: python run_all.py
"""

import os
import sys
import subprocess
import time
from pathlib import Path


TIMEOUT_SECONDS = 300  

def print_header(title):
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def check_dependencies():
    try:
        import pulp
        import numpy
        import matplotlib
        import sklearn
        import scipy
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def create_directory(path):
   
    Path(path).mkdir(parents=True, exist_ok=True)

def run_script(script_path, description, retry_count=1):
 
    print_header(f"Running: {description}")

    script_dir = os.path.dirname(script_path)
    if script_dir:
        create_directory(script_dir)
    
    for attempt in range(retry_count):
        try:
            # Run the script and capture output
            result = subprocess.run(
                [sys.executable, script_path], 
                capture_output=True, 
                text=True, 
                cwd=script_dir or '.',
                timeout=TIMEOUT_SECONDS
            )
            
           
            if result.stdout:
                print(result.stdout)
      
            if result.stderr:
                print("Warnings/Info:")
                print(result.stderr)
      
            if result.returncode == 0:
                return True
            else:
                print(f"⚠ Script exited with code {result.returncode}")
                if attempt < retry_count - 1:
                    print(f"Retrying... (attempt {attempt + 2}/{retry_count})")
                    time.sleep(2)
                continue
                
        except subprocess.TimeoutExpired:
            print(f"Error: {script_path} timed out after {TIMEOUT_SECONDS} seconds")
            if attempt < retry_count - 1:
                print(f"Retrying... (attempt {attempt + 2}/{retry_count})")
                time.sleep(2)
            continue
        except Exception as e:
            print(f"Error running {script_path}: {e}")
            if attempt < retry_count - 1:
                print(f"Retrying... (attempt {attempt + 2}/{retry_count})")
                time.sleep(2)
            continue
    
    return False

def verify_outputs():
   
    print_header("VERIFYING OUTPUTS")
    
    # All expected output files from all team members
    output_files = {
        # Bryan
        'bryan/test_plot.png': 'Bryan constraint test plot',
        
        # Deep
        'deep/simplex_step_1.png': 'Deep simplex step 1',
        'deep/simplex_step_2.png': 'Deep simplex step 2',
        'deep/simplex_step_3.png': 'Deep simplex step 3',
        'deep/all_steps_combined.png': 'Deep combined steps',
        
        # Jovan
        'Jovan/solution_plot.png': 'Jovan LP solution plot',
        
        # Japneet
        'japneet/solution_summary.txt': 'Japneet network LP summary',
        
        # Gurjas
        'Gurjas/pca_visualization.png': 'Gurjas PCA visualization',
        'Gurjas/parallel_coordinates.png': 'Gurjas parallel coordinates',
        'Gurjas/correlation_heatmap.png': 'Gurjas correlation heatmap',
    }
    
    found_files = []
    missing_files = []
    
    print("\nChecking output files...\n")
    
    for file_path, description in output_files.items():
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✓ {file_path} - {description} ({size} bytes)")
            found_files.append(file_path)
        else:
            print(f"✗ {file_path} - {description} NOT FOUND")
            missing_files.append(file_path)
    
    return len(found_files), len(output_files), found_files, missing_files

def print_summary(script_success, output_success, output_total, missing_files, elapsed):
  
    print_header("EXECUTION SUMMARY")
    
    print("\nScript Execution Results:")
    for description, success in script_success:
        status = "✓" if success else "✗"
        print(f"  {status} {description}")
    
    print(f"\nOutput Files: {output_success}/{output_total} found")
    
    if missing_files:
        print("\nMissing Files (may need to run scripts again):")
        for file_path in missing_files:
            print(f"  - {file_path}")
    
    print_header(f"COMPLETE - Elapsed time: {elapsed:.2f} seconds")
    
    print("\n" + "="*60)
    print(" NEXT STEPS")
    print("="*60)
    print("1. If all outputs were found, the integration is successful!")
    print("2. If some files are missing, ensure each team member's script runs individually")
    print("3. Create final bundle: git bundle create project.bundle main")
    print("4. Submit the bundle file as required by the assignment")

def main():
    """Main execution function - coordinates all team members' code"""
    print_header("LINEAR PROGRAMMING SIMPLEX VISUALIZATION")
    print("Project: Simplex Algorithm Visualization")
    print("Team: Bryan, Deep, Gurjas, Japneet, Jovan, Nishant")
    print("\nThis script coordinates execution of all team members' code.")
    print("="*60)
    
    if not check_dependencies():
        print("\nPlease install missing dependencies and try again.")
        sys.exit(1)
    
    start_time = time.time()
    
    scripts = [
        ('bryan/constraints.py', "Bryan's Constraint Helpers"),
        ('deep/simplex_2d.py', "Deep's 2D Simplex Visualization"),
        ('Jovan/library_solver.py', "Jovan's Library Solver (5+ constraints)"),
        ('japneet/network_lp.py', "Japneet's Network LP (long15.mps)"),
        ('gurjas/higher_dim_viz.py', "Gurjas Higher-Dimensional Visualization"),
    ]
    
    script_success = []
    for script_path, description in scripts:
        if os.path.exists(script_path):
            success = run_script(script_path, description, retry_count=1)
            script_success.append((description, success))
        else:
            print(f"Warning: {script_path} not found")
            print("Please ensure all team members have committed their code to the repository.")
            script_success.append((description, False))
    
    output_success, output_total, found_files, missing_files = verify_outputs()
    
    print_summary(script_success, output_success, output_total, missing_files, time.time() - start_time)
    
    all_scripts_success = all(success for _, success in script_success)
    all_outputs_found = output_success == output_total
    
    if all_scripts_success and all_outputs_found:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()