import os
import bz2
import urllib.request
print("RUNNING FILE")

DATA_DIR = "Japneet/data"
BZ2_PATH = os.path.join(DATA_DIR, "long15.mps.bz2")
MPS_PATH = os.path.join(DATA_DIR, "long15.mps")

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

    for line in lines[:1000]:  # sample first 1000 lines
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
        if len(parts) > 0:
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

def solve_lp(mps_path):
    print("\n" + "="*50)
    print("SOLVING LP")
    print("="*50)

    start = time.time()

    try:
        prob = pulp.LpProblem.fromMPS(mps_path)
    except Exception as e:
        print("Error reading MPS:", e)
        return None, None

    print(f"Loaded in {time.time() - start:.2f}s")

    solve_start = time.time()

    solver = pulp.PULP_CBC_CMD(msg=True, timeLimit=60)
    prob.solve(solver)

    solve_time = time.time() - solve_start

    status = pulp.LpStatus[prob.status]
    objective = pulp.value(prob.objective)

    result = {
        "status": status,
        "objective": objective,
        "solve_time": solve_time,
        "n_variables": len(prob.variables()),
        "n_constraints": len(prob.constraints)
    }

    return result, prob

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
    print(f"Variables: {result['n_variables']}")
    print(f"Constraints: {result['n_constraints']}")

    with open(OUTPUT_FILE, "w") as f:
        f.write("NETWORK LP SOLUTION SUMMARY\n")
        f.write("="*40 + "\n")
        f.write(f"Status: {result['status']}\n")
        f.write(f"Objective: {obj:.4f}\n")
        f.write(f"Solve Time: {result['solve_time']:.2f}s\n")
        f.write(f"Variables: {result['n_variables']}\n")
        f.write(f"Constraints: {result['n_constraints']}\n")

    print("\nSaved to japneet/solution_summary.txt")

def main():
    mps_path = download_and_extract()

    n_vars, n_cons = summarize_mps(mps_path)

    result, prob = solve_lp(mps_path)

    save_results(result, n_vars, n_cons)


if __name__ == "__main__":
    main()