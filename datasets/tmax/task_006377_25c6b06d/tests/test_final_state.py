# test_final_state.py

import os
import pytest
import csv
from collections import defaultdict

def test_c_source_exists():
    path = "/home/user/graph_analyzer.c"
    assert os.path.exists(path), f"Source file {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."

def test_executable_exists():
    path = "/home/user/graph_analyzer"
    assert os.path.exists(path), f"Executable {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_top_nodes_csv_content():
    input_csv = "/home/user/network_traffic.csv"
    output_csv = "/home/user/top_nodes.csv"

    assert os.path.exists(output_csv), f"Output file {output_csv} does not exist."
    assert os.path.isfile(output_csv), f"{output_csv} is not a file."

    # Compute expected output based on the input file
    assert os.path.exists(input_csv), f"Input file {input_csv} is missing."

    node_strengths = defaultdict(int)
    with open(input_csv, "r", newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if not row or len(row) < 4:
                continue
            src_ip = row[1]
            dst_ip = row[2]
            try:
                bytes_transferred = int(row[3])
            except ValueError:
                continue
            node_strengths[src_ip] += bytes_transferred
            node_strengths[dst_ip] += bytes_transferred

    # Filter >= 1000
    filtered_nodes = [(ip, strength) for ip, strength in node_strengths.items() if strength >= 1000]

    # Sort by strength descending, then IP alphabetically
    filtered_nodes.sort(key=lambda x: (-x[1], x[0]))

    # Limit to 2
    expected_top_nodes = filtered_nodes[:2]

    # Read actual output
    actual_top_nodes = []
    with open(output_csv, "r", newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            assert len(row) == 2, f"Row in {output_csv} does not have exactly 2 columns: {row}"
            ip = row[0].strip()
            try:
                strength = int(row[1].strip())
            except ValueError:
                pytest.fail(f"Invalid strength value in {output_csv}: {row[1]}")
            actual_top_nodes.append((ip, strength))

    assert actual_top_nodes == expected_top_nodes, (
        f"Content of {output_csv} is incorrect.\n"
        f"Expected: {expected_top_nodes}\n"
        f"Actual: {actual_top_nodes}"
    )