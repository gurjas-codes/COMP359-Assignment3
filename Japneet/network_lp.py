import os
import bz2
import urllib.request
import time
import subprocess

print("RUNNING FILE")

DATA_DIR = "Japneet/data"
BZ2_PATH = os.path.join(DATA_DIR, "long15.mps.bz2")
MPS_PATH = os.path.join(DATA_DIR, "long15.mps")
CBC_OUTPUT_FILE = "cbc_solution.txt"
SUMMARY_FILE = "solution_summary.txt"

def download_and_extract():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(BZ2_PATH):
        print("Downloading long15.mps.bz2...")
        url = "https://plato.asu.edu/ftp/lptestset/network/long15.mps.bz2"
        urllib.request.urlretrieve(url, BZ2_PATH)
        print("Download complete.")
    else:
        print("File already downloaded.")

    if not os.path.exists(MPS_PATH):
        print("Extracting file...")
        with bz2.open(BZ2_PATH, 'rb') as f_in:
            with open(MPS_PATH, 'wb') as f_out:
                f_out.write(f_in.read())
        print("Extraction complete.")
    else:
        print("File already extracted.")

    return MPS_PATH

def summarize_mps(mps_path):
    print("\n" + "="*50)
    print("MPS FILE SUMMARY")
    print("="*50)

    with open(mps_path, 'r') as f:
        lines = f.readlines()

    print(f"Total lines: {len(lines)}")

    sections = ['ROWS', 'COLUMNS', 'RHS', 'BOUNDS']
    current_section = None
    section_data = {s: [] for s in sections}

    for line in lines:
        line = line.strip()
        if line in sections:
            current_section = line
            continue
        if current_section:
            section_data[current_section].append(line)

    # Constraints
    constraints = section_data['ROWS']
    n_constraints = len(constraints)

    # Variables (unique)
    variables = set()
    for line in section_data['COLUMNS']:
        parts = line.split()
        if len(parts) > 1:
            variables.add(parts[0])

    n_variables = len(variables)

    print(f"Constraints: {n_constraints}")
    print(f"Variables (unique): {n_variables}")

    print("\nSample constraints:")
    for c in constraints[:5]:
        print(" ", c)

    print("\nSample variables:")
    for v in list(variables)[:5]:
        print(" ", v)

    return n_variables, n_constraints

def solve_lp_cbc(mps_path):
    print("\n" + "="*50)
    print("SOLVING LP USING CBC")
    print("="*50)

    start_time = time.time()

    # Run CBC solver directly
    try:
        subprocess.run(
            ["cbc", mps_path, "solve", "solu", CBC_OUTPUT_FILE],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except FileNotFoundError:
        print("CBC solver not found. Install it or add it to PATH.")
        return None
    except subprocess.CalledProcessError as e:
        print("Error running CBC:", e)
        return None

    solve_time = time.time() - start_time
    print(f"Solved in {solve_time:.2f}s")

    # Read objective value from CBC output
    objective = None
    try:
        with open(CBC_OUTPUT_FILE, "r") as f:
            for line in f:
                if "Objective value" in line:
                    objective = float(line.split()[-1])
                    break
    except:
        print("Could not read CBC solution file.")

    result = {
        "status": "Solved" if objective is not None else "Unknown",
        "objective": objective,
        "solve_time": solve_time,
        "n_variables": None,
        "n_constraints": None
    }

    return result

def save_results(result, n_vars, n_cons):
    print("\n" + "="*50)
    print("RESULT SUMMARY")
    print("="*50)

    if result is None:
        print("No solution found.")
        return

    obj = result["objective"] if result["objective"] is not None else 0

    print(f"Status: {result['status']}")
    print(f"Objective: {obj:.4f}")
    print(f"Solve Time: {result['solve_time']:.2f}s")
    print(f"Constraints: {n_cons}")
    print(f"Variables: {n_vars}")

    with open(SUMMARY_FILE, "w") as f:
        f.write("NETWORK LP SOLUTION SUMMARY\n")
        f.write("="*40 + "\n")
        f.write(f"Status: {result['status']}\n")
        f.write(f"Objective: {obj:.4f}\n")
        f.write(f"Solve Time: {result['solve_time']:.2f}s\n")
        f.write(f"Variables: {n_vars}\n")
        f.write(f"Constraints: {n_cons}\n")

    print(f"\nSaved to {SUMMARY_FILE}")

def main():
    mps_path = download_and_extract()
    n_vars, n_cons = summarize_mps(mps_path)
    result = solve_lp_cbc(mps_path)
    save_results(result, n_vars, n_cons)

if __name__ == "__main__":
    main()