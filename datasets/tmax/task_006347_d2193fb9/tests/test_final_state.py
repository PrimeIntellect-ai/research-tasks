# test_final_state.py

import os
import pytest

def test_path_csv_exists_and_correct():
    path_csv = "/home/user/path.csv"
    assert os.path.isfile(path_csv), f"Output file {path_csv} does not exist. Did you run your C++ program?"

    expected_content = """step,node_id,node_name,cumulative_weight
0,1,START,0
1,4,GAMMA,2
2,5,DELTA,4
3,6,END,8"""

    with open(path_csv, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {path_csv} does not match the expected shortest path output."

def test_cpp_source_exists():
    cpp_file = "/home/user/graph_solver.cpp"
    assert os.path.isfile(cpp_file), f"C++ source file {cpp_file} is missing."

def test_executable_exists():
    executable = "/home/user/graph_solver"
    assert os.path.isfile(executable), f"Compiled executable {executable} is missing."
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."