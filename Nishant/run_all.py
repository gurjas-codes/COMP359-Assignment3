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
            cwd=os.path.dirname(script_path) or '.'
        )
        
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("Errors/Warnings:")
            print(result.stderr)
        
        return True
        
    except Exception as e:
        print(f"Error running {script_path}: {e}")
        return False

def main():
    print_header("LINEAR PROGRAMMING SIMPLEX VISUALIZATION")
    print("Running all components...")
    
    start_time = time.time()
    
    # script list will be added here
    
    elapsed = time.time() - start_time
    print_header(f"COMPLETE - Elapsed time: {elapsed:.2f} seconds")

if __name__ == "__main__":
    main()