# test_final_state.py

import os

def test_c_source_and_executable_exist():
    source_path = "/home/user/workspace/analyze_graph.c"
    exec_path = "/home/user/workspace/analyze_graph"

    assert os.path.isfile(source_path), f"C source file {source_path} is missing."
    assert os.path.isfile(exec_path), f"Executable file {exec_path} is missing."
    assert os.access(exec_path, os.X_OK), f"File {exec_path} is not executable."

def test_top_authors_output():
    output_path = "/home/user/results/top_authors.txt"

    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "Bob:4",
        "Alice:3",
        "Charlie:3"
    ]

    assert len(lines) == 3, f"Expected exactly 3 lines in {output_path}, found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual}'."