# test_final_state.py

import os
import pytest

def test_c_source_exists():
    path = "/home/user/analyze_graph.c"
    assert os.path.isfile(path), f"C source file not found at {path}"

def test_executable_exists_and_executable():
    path = "/home/user/analyze_graph"
    assert os.path.isfile(path), f"Executable not found at {path}"
    assert os.access(path, os.X_OK), f"File at {path} is not executable"

def test_csv_output_correct():
    path = "/home/user/frequent_citations.csv"
    assert os.path.isfile(path), f"CSV output file not found at {path}"

    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    expected_content = (
        "Citing_Author_Name,Cited_Author_Name,Citation_Count\n"
        "Alice,Charlie,3\n"
        "Eve,Alice,2"
    )

    # Normalize line endings
    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, f"CSV content does not match expected output.\nExpected:\n{expected_content}\n\nActual:\n{content}"