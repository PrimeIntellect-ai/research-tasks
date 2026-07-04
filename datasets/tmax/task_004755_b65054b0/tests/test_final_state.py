# test_final_state.py
import os
import math

def test_results_txt_exists():
    assert os.path.exists("/home/user/results.txt"), "/home/user/results.txt does not exist."
    assert os.path.isfile("/home/user/results.txt"), "/home/user/results.txt is not a file."

def test_results_txt_content():
    pdb_path = "/home/user/protein.pdb"
    assert os.path.exists(pdb_path), f"Input file {pdb_path} is missing."

    # 1. Parse PDB for Z-coordinates
    z_coords = []
    with open(pdb_path, "r") as f:
        for line in f:
            if line.startswith("ATOM"):
                # columns 47-54 (1-indexed) -> index 46:54
                z_str = line[46:54].strip()
                z_coords.append(float(z_str))

    assert len(z_coords) > 0, "No ATOM lines found in PDB file."

    # 2. Domain Definition
    z_min = min(z_coords)
    z_max = max(z_coords)
    z_start = math.floor(z_min)
    z_end = math.ceil(z_max)

    # 3. Mesh Refinement
    cells = []
    dx_min = 1.0
    for i in range(int(z_start), int(z_end)):
        lower = float(i)
        upper = lower + 1.0

        # Check if cell contains any atom
        contains_atom = False
        for z in z_coords:
            if lower <= z < upper:
                contains_atom = True
                break
            # Last cell inclusive upper bound
            if upper == z_end and z == upper:
                contains_atom = True
                break

        if contains_atom:
            cells.append((lower, lower + 0.5, 0.5))
            cells.append((lower + 0.5, upper, 0.5))
            dx_min = 0.5
        else:
            cells.append((lower, upper, 1.0))

    # 4. Domain Decomposition
    midpoint_space = (z_start + z_end) / 2.0
    domain1_cells = 0
    domain2_cells = 0
    integral = 0.0

    for lower, upper, width in cells:
        mid = (lower + upper) / 2.0
        if mid < midpoint_space:
            domain1_cells += 1
        else:
            domain2_cells += 1

        # 5. Numerical Integration
        integral += (mid ** 2) * width

    # 6. Numerical Stability
    dt = 0.2
    is_stable = dt <= (dx_min ** 2) / 2.0
    stability_str = "STABLE" if is_stable else "UNSTABLE"

    expected_output = (
        f"Total Atoms: {len(z_coords)}\n"
        f"Z_min: {z_min:.4f}\n"
        f"Z_max: {z_max:.4f}\n"
        f"Domain 1 Cells: {domain1_cells}\n"
        f"Domain 2 Cells: {domain2_cells}\n"
        f"Integral: {integral:.4f}\n"
        f"Stability dt=0.2: {stability_str}\n"
    )

    with open("/home/user/results.txt", "r") as f:
        actual_output = f.read().strip()

    expected_stripped = expected_output.strip()

    assert actual_output == expected_stripped, (
        f"Results do not match expected output.\n"
        f"Expected:\n{expected_stripped}\n\n"
        f"Actual:\n{actual_output}"
    )