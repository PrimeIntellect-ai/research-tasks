# test_final_state.py

import os

def test_result_file():
    """Verify the final result.txt against the derived mathematical solution."""
    pdb_path = "/home/user/protein.pdb"
    assert os.path.exists(pdb_path), f"PDB file is missing: {pdb_path}"

    # 1. & 2. Extract CA coordinates
    ca_coords = []
    with open(pdb_path, "r") as f:
        for line in f:
            parts = line.split()
            # In the provided PDB format, space-separated columns:
            # 0: ATOM, 1: serial, 2: name (CA), 3: resName, 4: chainID, 5: resSeq, 6: X, 7: Y, 8: Z
            # Wait, the task says: "3rd space-separated column ... 6th, 7th, 8th"
            # Let's strictly follow the task's space-separated column indexing (0-indexed or 1-indexed? Usually 1-indexed in task descriptions).
            # "3rd space-separated column" -> parts[2]
            # "6th, 7th, 8th" -> parts[5], parts[6], parts[7]
            if len(parts) >= 8 and parts[0] == "ATOM" and parts[2] == "CA":
                ca_coords.append([float(parts[5]), float(parts[6]), float(parts[7])])
                if len(ca_coords) == 3:
                    break

    assert len(ca_coords) == 3, "Could not find exactly 3 CA atoms in the PDB file."

    # 3. Matrix A and LU Decomposition (Doolittle)
    A = ca_coords
    n = 3
    L = [[0.0] * n for _ in range(n)]
    U = [[0.0] * n for _ in range(n)]

    for i in range(n):
        L[i][i] = 1.0
        for k in range(i, n):
            sum_val = sum(L[i][j] * U[j][k] for j in range(i))
            U[i][k] = A[i][k] - sum_val
        for k in range(i + 1, n):
            sum_val = sum(L[k][j] * U[j][i] for j in range(i))
            L[k][i] = (A[k][i] - sum_val) / U[i][i]

    # 4. Forward Euler
    # y(0.1) = y(0) + 0.1 * L * y(0)
    y0 = [1.0, 1.0, 1.0]
    dt = 0.1

    y1 = [0.0] * n
    for i in range(n):
        Ly_i = sum(L[i][j] * y0[j] for j in range(n))
        y1[i] = y0[i] + dt * Ly_i

    expected_str = f"{y1[0]:.4f} {y1[1]:.4f} {y1[2]:.4f}"

    result_path = "/home/user/result.txt"
    assert os.path.exists(result_path), f"Result file not found: {result_path}"

    with open(result_path, "r") as f:
        result_content = f.read().strip()

    assert result_content == expected_str, f"Expected '{expected_str}' in {result_path}, but got '{result_content}'"