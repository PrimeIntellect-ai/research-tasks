# test_final_state.py

import os
import re
import subprocess
import pytest
import numpy as np

def extract_ca_chain_a(pdb_path):
    coords = []
    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith("ATOM  "):
                atom_name = line[12:16].strip()
                chain_id = line[21]
                if atom_name == "CA" and chain_id == "A":
                    try:
                        x = float(line[30:38])
                        y = float(line[38:46])
                        z = float(line[46:54])
                        coords.append([x, y, z])
                    except ValueError:
                        pass
    return np.array(coords)

def compute_expected_radius(coords):
    if len(coords) < 3:
        return 0.0

    # 1. Center the points
    mean = np.mean(coords, axis=0)
    centered = coords - mean

    # 2. SVD to find the plane and 2D basis
    U, S, Vt = np.linalg.svd(centered, full_matrices=False)

    # The normal is the last row of Vt (smallest singular value)
    # The 2D basis is the first two rows of Vt
    basis = Vt[:2, :]

    # 3. Project points onto the 2D basis
    proj = centered @ basis.T

    x = proj[:, 0]
    y = proj[:, 1]

    # 4. Fit circle using Kåsa method: x^2 + y^2 = 2ax + 2by + c
    A = np.column_stack((2 * x, 2 * y, np.ones_like(x)))
    b = x**2 + y**2

    res, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
    a, b_val, c = res

    # 5. Compute radius
    R = np.sqrt(a**2 + b_val**2 + c)
    return R

def create_test_pdb(path):
    # Generate points roughly on a circle with some noise and 3D rotation
    angles = np.linspace(0, 2 * np.pi, 20, endpoint=False)
    r = 12.345
    x = r * np.cos(angles)
    y = r * np.sin(angles)
    z = 0.5 * np.sin(3 * angles) # slight deviation from a perfect plane

    # Rotate in 3D
    R_mat = np.array([
        [0.36, 0.48, -0.8],
        [-0.8, 0.60,  0.0],
        [0.48, 0.64,  0.6]
    ])
    coords = np.column_stack((x, y, z)) @ R_mat.T

    # Translate
    coords += np.array([10.0, -5.0, 20.0])

    with open(path, 'w') as f:
        for i, (cx, cy, cz) in enumerate(coords):
            f.write(f"ATOM  {i+1:5d}  CA  ALA A{i+1:4d}    {cx:8.3f}{cy:8.3f}{cz:8.3f}  1.00  0.00           C  \n")
        # Add some decoy atoms
        f.write(f"ATOM  {100:5d}  CB  ALA A{100:4d}    {0.0:8.3f}{0.0:8.3f}{0.0:8.3f}  1.00  0.00           C  \n")
        f.write(f"ATOM  {101:5d}  CA  ALA B{101:4d}    {0.0:8.3f}{0.0:8.3f}{0.0:8.3f}  1.00  0.00           C  \n")

def test_files_exist():
    source_path = "/home/user/fit_loop.c"
    binary_path = "/home/user/fit_loop"

    assert os.path.isfile(source_path), f"Source file {source_path} does not exist."
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_circle_fitting_accuracy():
    binary_path = "/home/user/fit_loop"
    test_pdb_path = "/tmp/test_eval.pdb"

    create_test_pdb(test_pdb_path)

    coords = extract_ca_chain_a(test_pdb_path)
    expected_radius = compute_expected_radius(coords)

    try:
        result = subprocess.run([binary_path, test_pdb_path], capture_output=True, text=True, timeout=10)
    except subprocess.TimeoutExpired:
        pytest.fail("The C program timed out after 10 seconds.")

    assert result.returncode == 0, f"Program exited with non-zero status code: {result.returncode}\nStderr: {result.stderr}"

    match = re.search(r"Radius:\s*([0-9.]+)", result.stdout)
    assert match, f"Could not find 'Radius: <float>' in output.\nOutput was: {result.stdout}"

    agent_radius = float(match.group(1))
    error = abs(agent_radius - expected_radius)

    threshold = 0.001
    assert error <= threshold, (
        f"Radius error is too high.\n"
        f"Expected: {expected_radius:.4f}\n"
        f"Got:      {agent_radius:.4f}\n"
        f"Error:    {error:.5f} (Threshold: {threshold})"
    )