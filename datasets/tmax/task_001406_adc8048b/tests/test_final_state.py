# test_final_state.py

import os
import pytest

def test_process_cpp_exists():
    assert os.path.isfile("/home/user/process.cpp"), "The file /home/user/process.cpp is missing."

def test_nodes_csv():
    nodes_csv_path = "/home/user/nodes.csv"
    assert os.path.isfile(nodes_csv_path), f"The file {nodes_csv_path} is missing."

    with open(nodes_csv_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "1,Alpha,1",
        "2,Beta,2",
        "3,Gamma,2",
        "5,Epsilon,1"
    ]

    # Remove header if present
    if lines and (lines[0].lower().startswith("id") or lines[0].lower().startswith("c_id")):
        lines = lines[1:]

    assert lines == expected_lines, f"The content of {nodes_csv_path} does not match the expected output."

def test_edges_csv():
    edges_csv_path = "/home/user/edges.csv"
    assert os.path.isfile(edges_csv_path), f"The file {edges_csv_path} is missing."

    with open(edges_csv_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "1,2,6.5",
        "2,3,5.5",
        "3,5,5.1"
    ]

    # Remove header if present
    if lines and (lines[0].lower().startswith("src") or lines[0].lower().startswith("c_a")):
        lines = lines[1:]

    # Floating point representations might differ slightly (e.g., 6.5 vs 6.50), but standard output should match
    # Let's parse and compare
    parsed_lines = []
    for line in lines:
        parts = line.split(',')
        if len(parts) == 3:
            parsed_lines.append((int(parts[0]), int(parts[1]), float(parts[2])))
        else:
            parsed_lines.append(line)

    expected_parsed = [
        (1, 2, 6.5),
        (2, 3, 5.5),
        (3, 5, 5.1)
    ]

    assert parsed_lines == expected_parsed, f"The content of {edges_csv_path} does not match the expected output."