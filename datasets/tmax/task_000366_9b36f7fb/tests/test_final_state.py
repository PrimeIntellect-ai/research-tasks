# test_final_state.py

import os
import math
import pytest

def test_eigen_downloaded_and_extracted():
    """Test that Eigen source is extracted to the correct directory."""
    eigen_dir = "/home/user/eigen_src"
    assert os.path.isdir(eigen_dir), f"Eigen directory missing: {eigen_dir}"

    # Check for core Eigen headers
    eigen_core_path = os.path.join(eigen_dir, "Eigen", "Core")
    # Sometimes it extracts into an inner directory like eigen-3.4.0
    # Let's just search for the Eigen/Core file inside eigen_src
    found_core = False
    for root, dirs, files in os.walk(eigen_dir):
        if "Core" in files and os.path.basename(root) == "Eigen":
            found_core = True
            break
    assert found_core, "Could not find Eigen/Core headers in /home/user/eigen_src"

def test_cpp_code_exists():
    """Test that the C++ source file exists."""
    cpp_path = "/home/user/workspace/extract_features.cpp"
    assert os.path.isfile(cpp_path), f"C++ source file missing: {cpp_path}"

def test_executable_exists():
    """Test that the compiled executable exists and is executable."""
    exe_path = "/home/user/workspace/ml_feat_prep"
    assert os.path.isfile(exe_path), f"Executable missing: {exe_path}"
    assert os.access(exe_path, os.X_OK), f"File is not executable: {exe_path}"

def compute_ground_truth():
    """Compute the ground truth values from the given PDB coordinates."""
    coords = [
        [11.0, 10.0, 10.0],
        [13.0, 11.0, 11.0],
        [15.0, 12.0, 12.0],
        [17.0, 13.0, 13.0],
        [19.0, 14.0, 14.0],
        [21.0, 15.0, 15.0],
        [23.0, 16.0, 16.0],
        [25.0, 17.0, 17.0],
        [27.0, 18.0, 18.0],
        [29.0, 19.0, 19.0]
    ]
    n = len(coords)
    D = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dist = math.sqrt(sum((coords[i][k] - coords[j][k])**2 for k in range(3)))
            D[i][j] = dist

    # Compute SVD using a simple power iteration or just hardcode the known values 
    # since we can't use numpy. The prompt gives the exact expected values anyway.
    # We will just yield the expected lines as given in the prompt's truth verification.

    expected_lines = []
    expected_lines.append("56.3323,11.3326,4.4925")

    for i in range(n):
        distances = []
        for j in range(n):
            if i == j:
                continue
            distances.append((D[i][j], j))
        # Sort by distance, then by index
        distances.sort(key=lambda x: (x[0], x[1]))
        neighbors = [x[1] for x in distances[:3]]
        expected_lines.append(f"{i},{neighbors[0]},{neighbors[1]},{neighbors[2]}")

    return expected_lines

def test_output_csv_content():
    """Test that the generated CSV file exactly matches the expected ground truth."""
    csv_path = "/home/user/output/features.csv"
    assert os.path.isfile(csv_path), f"Output CSV missing: {csv_path}"

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = compute_ground_truth()

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in CSV, found {len(lines)}"

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Mismatch on line {i+1}. Expected: '{expected}', Actual: '{actual}'"