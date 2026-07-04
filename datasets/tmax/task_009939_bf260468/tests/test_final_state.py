# test_final_state.py

import os
import pytest

CPP_FILE = "/home/user/process_graph.cpp"
EXE_FILE = "/home/user/process_graph"
OUTPUT_FILE = "/home/user/final_edges.csv"

def test_cpp_file_exists():
    assert os.path.isfile(CPP_FILE), f"C++ source file {CPP_FILE} does not exist."

def test_executable_exists():
    assert os.path.isfile(EXE_FILE), f"Executable {EXE_FILE} does not exist. Did you compile the C++ program?"
    assert os.access(EXE_FILE, os.X_OK), f"File {EXE_FILE} is not executable."

def test_final_edges_output():
    assert os.path.isfile(OUTPUT_FILE), f"Output file {OUTPUT_FILE} does not exist."

    with open(OUTPUT_FILE, "r") as f:
        content = f.read().strip()

    assert content, f"Output file {OUTPUT_FILE} is empty."

    lines = content.split('\n')
    actual_data = []
    for line in lines:
        if not line.strip():
            continue
        parts = line.split(',')
        assert len(parts) == 3, f"Line '{line}' does not have exactly 3 comma-separated values."
        try:
            actual_data.append((float(parts[0]), float(parts[1]), float(parts[2])))
        except ValueError:
            pytest.fail(f"Could not parse line '{line}' as floats.")

    expected_data = [
        (1.0, 2.0, 12.0),
        (2.0, 3.0, 15.0),
        (4.0, 1.0, 11.0)
    ]

    assert actual_data == expected_data, f"Data in {OUTPUT_FILE} does not match expected output. Got {actual_data}, expected {expected_data}."