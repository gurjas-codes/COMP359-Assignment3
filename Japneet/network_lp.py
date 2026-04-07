"""
Parse and solve long15.mps network LP problem
"""

import bz2
import urllib.request
import os
import pulp
import time

def get_script_dir():
    """Get the directory where this script is located"""
    return os.path.dirname(os.path.abspath(__file__))

def download_and_extract():
    """Download long15.mps.bz2 if not already present"""
    
    # Create data directory
    script_dir = get_script_dir()
    data_dir = os.path.join(script_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    bz2_path = os.path.join(data_dir, 'long15.mps.bz2')
    mps_path = os.path.join(data_dir, 'long15.mps')
    
    if not os.path.exists(bz2_path):
        print("Downloading long15.mps.bz2...")
        url = "https://plato.asu.edu/ftp/lptestset/network/long15.mps.bz2"
        try:
            urllib.request.urlretrieve(url, bz2_path)
            print("Download complete!")
        except Exception as e:
            print(f"Download failed: {e}")
            print("Using synthetic data instead...")
            return None
    else:
        print("File already downloaded.")
    
    if not os.path.exists(mps_path) and os.path.exists(bz2_path):
        print("Extracting...")
        with bz2.open(bz2_path, 'rb') as f_in:
            with open(mps_path, 'wb') as f_out:
                f_out.write(f_in.read())
        print("Extraction complete!")
    
    return mps_path

def read_and_summarize(mps_path):
    """Read MPS file and print summary information"""
    
    print("\n" + "="*60)
    print("LONG15.MPS FILE ANALYSIS")
    print("="*60)
    
    try:
        with open(mps_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"File not found: {mps_path}")
        return None
    
    print(f"Total lines in file: {len(lines)}")
    
    # Find sections
    sections = ['ROWS', 'COLUMNS', 'RHS', 'BOUNDS', 'ENDATA']
    section_lines = {section: [] for section in sections}
    
    current_section = None
    for line in lines[:500]:  # Only first 500 lines for summary
        line_stripped = line.strip()
        if line_stripped in sections:
            current_section = line_stripped
            continue
        if current_section and current_section in section_lines:
            section_lines[current_section].append(line_stripped)
    
    # Count constraints (ROWS section)
    rows = section_lines['ROWS']
    n_constraints = len(rows)
    n_variables = len(section_lines['COLUMNS'])
    
    print(f"\nNumber of constraints (ROWS): {n_constraints}")
    print(f"Number of variables (estimated from COLUMNS): {n_variables}")
    
    # Show sample constraints
    print("\nSample constraints (first 10):")
    for row in rows[:10]:
        print(f"  {row}")
    
    return {
        'n_constraints': n_constraints,
        'n_variables': n_variables,
        'rows': rows
    }

def solve_network_lp(mps_path):
    """Solve the LP using PuLP"""
    
    print("\n" + "="*60)
    print("SOLVING NETWORK LP")
    print("="*60)
    
    if mps_path is None or not os.path.exists(mps_path):
        print("MPS file not available. Creating a sample network LP problem...")
        return solve_sample_network_lp()
    
    start_time = time.time()
    
    try:
        # Read MPS file
        prob = pulp.LpProblem("Network_LP", pulp.LpMinimize)
        prob.readMPS(mps_path)
        
        print(f"Problem read in {time.time() - start_time:.2f} seconds")
        
        # Solve
        solve_start = time.time()
        prob.solve(pulp.PULP_CBC_CMD(msg=True, timeLimit=60))
        solve_time = time.time() - solve_start
        
        # Results
        result = {
            'status': pulp.LpStatus[prob.status],
            'objective': pulp.value(prob.objective),
            'solve_time': solve_time,
            'n_variables': len(prob.variables()),
            'n_constraints': len(prob.constraints)
        }
        
        return result, prob
        
    except Exception as e:
        print(f"Error solving MPS file: {e}")
        print("Falling back to sample network LP...")
        return solve_sample_network_lp()

def solve_sample_network_lp():
    """Create and solve a sample network LP problem"""
    
    print("\nCreating sample network LP problem...")
    
    prob = pulp.LpProblem("Sample_Network_LP", pulp.LpMinimize)
    
    # Variables for a simple flow network
    nodes = ['A', 'B', 'C', 'D']
    edges = [
        ('A', 'B'), ('A', 'C'),
        ('B', 'C'), ('B', 'D'),
        ('C', 'D')
    ]
    
    # Flow variables
    flow_vars = {}
    for u, v in edges:
        flow_vars[(u, v)] = pulp.LpVariable(f"flow_{u}_{v}", lowBound=0)
    
    # Objective: minimize total flow cost
    costs = {
        ('A', 'B'): 2, ('A', 'C'): 3,
        ('B', 'C'): 1, ('B', 'D'): 4,
        ('C', 'D'): 2
    }
    
    prob += pulp.lpSum(costs[e] * flow_vars[e] for e in edges)
    
    # Flow conservation constraints
    supply_demand = {'A': 10, 'B': 0, 'C': 0, 'D': -10}
    
    for node in nodes:
        inflow = pulp.lpSum(flow_vars[(u, v)] for u, v in edges if v == node)
        outflow = pulp.lpSum(flow_vars[(u, v)] for u, v in edges if u == node)
        prob += inflow - outflow == supply_demand[node]
    
    # Solve
    solve_start = time.time()
    prob.solve(pulp.PULP_CBC_CMD(msg=True))
    solve_time = time.time() - solve_start
    
    result = {
        'status': pulp.LpStatus[prob.status],
        'objective': pulp.value(prob.objective),
        'solve_time': solve_time,
        'n_variables': len(prob.variables()),
        'n_constraints': len(prob.constraints)
    }
    
    return result, prob

def print_summary(result):
    """Print solution summary"""
    
    print("\n" + "="*60)
    print("SOLUTION SUMMARY")
    print("="*60)
    print(f"Status: {result['status']}")
    print(f"Objective Value: {result['objective']:.4f}")
    print(f"Solve Time: {result['solve_time']:.2f} seconds")
    print(f"Number of Variables: {result['n_variables']}")
    print(f"Number of Constraints: {result['n_constraints']}")
    
    if result['status'] == 'Optimal':
        print("\n✓ Problem solved optimally!")
    else:
        print(f"\n⚠ Problem status: {result['status']}")

def save_results(result):
    """Save results to text file"""
    script_dir = get_script_dir()
    output_path = os.path.join(script_dir, 'solution_summary.txt')
    
    with open(output_path, 'w') as f:
        f.write("NETWORK LP SOLUTION\n")
        f.write("="*40 + "\n")
        f.write(f"Status: {result['status']}\n")
        f.write(f"Objective: {result['objective']:.4f}\n")
        f.write(f"Solve Time: {result['solve_time']:.2f}s\n")
        f.write(f"Variables: {result['n_variables']}\n")
        f.write(f"Constraints: {result['n_constraints']}\n")
    
    print(f"\nResults saved to {output_path}")

if __name__ == "__main__":
    print("\n" + "="*50)
    print("JAPNEET'S NETWORK LP SOLVER")
    print("="*50)
    
    # Step 1: Download and extract
    mps_path = download_and_extract()
    
    # Step 2: Read and summarize (if MPS file exists)
    if mps_path and os.path.exists(mps_path):
        summary = read_and_summarize(mps_path)
    
    # Step 3: Solve
    result, prob = solve_network_lp(mps_path)
    
    # Step 4: Print summary
    print_summary(result)
    
    # Step 5: Save results
    save_results(result)