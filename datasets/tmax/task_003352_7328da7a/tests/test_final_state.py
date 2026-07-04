# test_final_state.py

import os
import pytest
from collections import defaultdict

def test_source_file_exists():
    """Test that the C source file exists."""
    assert os.path.exists("/home/user/graph_analyzer.c"), "The source file /home/user/graph_analyzer.c does not exist."

def test_executable_exists():
    """Test that the compiled executable exists and is executable."""
    exe_path = "/home/user/graph_analyzer"
    assert os.path.exists(exe_path), f"The executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"The file {exe_path} is not executable."

def test_output_file_exists():
    """Test that the output log file exists."""
    log_path = "/home/user/critical_nodes.log"
    assert os.path.exists(log_path), f"The output file {log_path} does not exist."

def test_output_contents():
    """Test that the output file contains the correctly computed, sorted, and paginated results."""
    edges_path = "/home/user/etl_edges.txt"
    log_path = "/home/user/critical_nodes.log"

    assert os.path.exists(edges_path), f"Input file {edges_path} is missing."
    assert os.path.exists(log_path), f"Output file {log_path} is missing."

    # Compute expected output
    out_degrees = defaultdict(int)
    with open(edges_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                src = int(parts[0])
                out_degrees[src] += 1

    min_degree = 10
    offset = 5
    page_size = 10

    filtered = [(node, degree) for node, degree in out_degrees.items() if degree >= min_degree]
    # Sort by descending out-degree, then ascending node ID
    filtered.sort(key=lambda x: (-x[1], x[0]))

    paginated = filtered[offset : offset + page_size]
    expected_lines = [f"{node}: {degree}" for node, degree in paginated]

    # Read actual output
    with open(log_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {log_path} do not match the expected output.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )