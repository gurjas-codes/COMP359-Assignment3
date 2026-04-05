import os
import sys
import subprocess
import time

def print_header(title):
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def run_script(script_path, description):

    print_header(f"Running: {description}")
    
    try:
        result = subprocess.run(
            [sys.executable, script_path], 
            capture_output=True, 
            text=True, 
            cwd=os.path.dirname(script_path) or '.',
            timeout=300  
        )
        
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("Errors/Warnings:")
            print(result.stderr)
        
        if result.returncode != 0:
            print(f"⚠ Script exited with code {result.returncode}")
            return False
        
        return True
        
    except subprocess.TimeoutExpired:
        print(f"Error: {script_path} timed out after 300 seconds")
        return False
    except Exception as e:
        print(f"Error running {script_path}: {e}")
        return False

def verify_outputs():

    print_header("VERIFYING OUTPUTS")
    
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
    print("\nNote: Some files may be created by subsequent runs or require")
    print("      dependencies to be installed. Run 'pip install -r requirements.txt'")

def main():
    print_header("LINEAR PROGRAMMING SIMPLEX VISUALIZATION")
    print("Running all components...")
    print("This script will execute all team members' code sequentially.")
    print("Make sure all dependencies are installed: pip install -r requirements.txt")
    
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
            success = run_script(script_path, description)
            script_success.append((description, success))
        else:
            print(f"Warning: {script_path} not found")
            script_success.append((description, False))
    
  
    output_success, output_total, found_files, missing_files = verify_outputs()
    
  
    print_summary(script_success, output_success, output_total, missing_files, time.time() - start_time)

if __name__ == "__main__":
    main()