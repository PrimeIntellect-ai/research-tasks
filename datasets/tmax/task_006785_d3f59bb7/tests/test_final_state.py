# test_final_state.py

import os
import struct
import re
import pytest

def test_results_and_code_exist():
    """Check that the C source, executable, and results log exist."""
    assert os.path.exists("/home/user/process_embeddings.c"), "C source file is missing."
    assert os.path.exists("/home/user/process_embeddings"), "Compiled executable is missing."
    assert os.path.exists("/home/user/results.log"), "Results log file is missing."

def test_results_content():
    """Parse results.log and verify the values against the expected computation."""
    log_path = "/home/user/results.log"
    assert os.path.exists(log_path), "Results log file is missing."

    with open(log_path, "r") as f:
        log_content = f.read().strip().splitlines()

    assert len(log_content) >= 3, "results.log must contain at least 3 lines."

    centroid_line = log_content[0]
    indices_line = log_content[1]
    time_line = log_content[2]

    assert centroid_line.startswith("Centroid: "), "First line must start with 'Centroid: '"
    assert indices_line.startswith("Closest Indices: "), "Second line must start with 'Closest Indices: '"
    assert time_line.startswith("Search Time: ") and time_line.endswith(" us"), "Third line must format Search Time correctly."

    # Compute expected indices
    embeddings_path = "/home/user/embeddings.bin"
    assert os.path.exists(embeddings_path), "embeddings.bin is missing."

    with open(embeddings_path, "rb") as f:
        data = f.read()

    num_vectors = 100000
    dim = 16
    assert len(data) == num_vectors * dim * 4, "embeddings.bin has unexpected size."

    floats = struct.unpack(f"{num_vectors * dim}f", data)
    vectors = [floats[i * dim : (i + 1) * dim] for i in range(num_vectors)]

    # Use LCG to count frequencies of each index
    counts = [0] * num_vectors
    state = 42
    for _ in range(100 * num_vectors):
        state = (state * 1664525 + 1013904223) & 0xFFFFFFFF
        counts[state % num_vectors] += 1

    # Compute centroid
    bootstrapped_centroid = [0.0] * dim
    for i in range(num_vectors):
        if counts[i] > 0:
            vec = vectors[i]
            c = counts[i]
            for d in range(dim):
                bootstrapped_centroid[d] += vec[d] * c

    for d in range(dim):
        bootstrapped_centroid[d] /= (100.0 * num_vectors)

    # Compute distances
    distances = []
    for i in range(num_vectors):
        vec = vectors[i]
        dist_sq = sum((vec[d] - bootstrapped_centroid[d]) ** 2 for d in range(dim))
        distances.append((dist_sq, i))

    distances.sort(key=lambda x: x[0])
    expected_closest = [x[1] for x in distances[:5]]
    expected_indices_str = "Closest Indices: " + ", ".join(map(str, expected_closest))

    assert indices_line == expected_indices_str, f"Expected '{expected_indices_str}', but got '{indices_line}'"