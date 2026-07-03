# test_final_state.py

import os
import math
import ctypes
import pytest

def test_c_source_and_executable_exist():
    """Test that the C source code and compiled executable exist."""
    src_path = "/home/user/src/search.c"
    exe_path = "/home/user/src/search"

    assert os.path.isfile(src_path), f"C source file {src_path} is missing."
    assert os.path.isfile(exe_path), f"Compiled executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_output_file_exists():
    """Test that the output file exists."""
    output_path = "/home/user/output/recommendations.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

def test_recommendations_content():
    """Test that the recommendations match the expected output derived from the data."""
    output_path = "/home/user/output/recommendations.txt"
    data_path = "/home/user/data/vectors.csv"

    assert os.path.isfile(data_path), f"Data file {data_path} is missing."
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    # Recompute the expected recommendations
    libc = ctypes.CDLL("libc.so.6")
    libc.srand(2024)

    # Generate matrix M (5x2)
    M = [[0.0, 0.0] for _ in range(5)]
    for i in range(5):
        for j in range(2):
            M[i][j] = (libc.rand() % 1000) / 1000.0

    # Read vectors
    vectors = {}
    with open(data_path, "r") as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split(',')
            vec_id = int(parts[0])
            vec_vals = [float(x) for x in parts[1:]]
            vectors[vec_id] = vec_vals

    # Project vectors
    projected = {}
    for vec_id, vec in vectors.items():
        p0 = sum(vec[k] * M[k][0] for k in range(5))
        p1 = sum(vec[k] * M[k][1] for k in range(5))
        projected[vec_id] = (p0, p1)

    # Calculate distances to id=42
    assert 42 in projected, "Item with id=42 not found in dataset."
    target_p = projected[42]
    distances = []
    for vec_id, p in projected.items():
        if vec_id == 42:
            continue
        dist = math.sqrt((p[0] - target_p[0])**2 + (p[1] - target_p[1])**2)
        distances.append((vec_id, dist))

    # Sort by distance, then id
    distances.sort(key=lambda x: (x[1], x[0]))

    expected_lines = [f"{distances[i][0]},{distances[i][1]:.4f}" for i in range(3)]

    # Read student output
    with open(output_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == 3, f"Expected exactly 3 lines in {output_path}, but found {len(actual_lines)}."

    for i in range(3):
        assert actual_lines[i] == expected_lines[i], (
            f"Line {i+1} mismatch: expected '{expected_lines[i]}', got '{actual_lines[i]}'."
        )