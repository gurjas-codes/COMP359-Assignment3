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

def verify_outputs(output_files):
    print_header("VERIFYING OUTPUTS")
    
    success_count = 0
    for file_path in output_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✓ {file_path} ({size} bytes)")
            success_count += 1
        else:
            print(f"✗ {file_path} not found")
    
    return success_count, len(output_files)

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
    
    output_files = [
        'bryan/test_plot.png',
        'deep/all_steps_combined.png',
        'Jovan/solution_plot.png',
        'japneet/solution_summary.txt',
        'Gurjas/pca_visualization.png',
    ]
    
    output_success, output_total = verify_outputs(output_files)
    
    print_header("EXECUTION SUMMARY")
    print("\nScript Execution Results:")
    for description, success in script_success:
        status = "✓" if success else "✗"
        print(f"  {status} {description}")
    
    print(f"\nOutput Files: {output_success}/{output_total} found")
    
    elapsed = time.time() - start_time
    print_header(f"COMPLETE - Elapsed time: {elapsed:.2f} seconds")

if __name__ == "__main__":
    main()