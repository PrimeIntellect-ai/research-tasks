# test_final_state.py
import os
import pytest

def test_cpp_file_exists():
    cpp_path = "/home/user/process_graph.cpp"
    assert os.path.exists(cpp_path), f"The C++ source file {cpp_path} is missing."
    assert os.path.isfile(cpp_path), f"{cpp_path} is not a file."

def test_output_file_exists_and_correct():
    out_path = "/home/user/optimized_path.txt"
    assert os.path.exists(out_path), f"The output file {out_path} is missing. Did you run your C++ program?"
    assert os.path.isfile(out_path), f"{out_path} is not a file."

    with open(out_path, "r") as f:
        content = f.read().strip()

    expected = "START->JOB_A->JOB_B->END"
    assert content == expected, f"The content of {out_path} is incorrect. Expected '{expected}', got '{content}'."