# test_final_state.py

import os
import re
import pytest

def test_cpp_source_exists():
    cpp_path = "/home/user/compute_cov.cpp"
    assert os.path.exists(cpp_path), f"C++ source file {cpp_path} does not exist."
    assert os.path.isfile(cpp_path), f"{cpp_path} is not a file."

def test_executable_exists_and_executable():
    exe_path = "/home/user/compute_cov"
    assert os.path.exists(exe_path), f"Executable {exe_path} does not exist. Did you compile the code?"
    assert os.path.isfile(exe_path), f"{exe_path} is not a file."
    assert os.access(exe_path, os.X_OK), f"{exe_path} is not executable."

def test_output_file_contents():
    output_path = "/home/user/cov_stats.txt"
    assert os.path.exists(output_path), f"Output file {output_path} does not exist. Did you run the program?"
    assert os.path.isfile(output_path), f"{output_path} is not a file."

    with open(output_path, "r") as f:
        content = f.read()

    # We expect Trace: 70.00 and TopLeft: 10.00
    # Use regex or string matching to be slightly flexible with whitespace
    trace_match = re.search(r"Trace:\s*70\.00", content)
    topleft_match = re.search(r"TopLeft:\s*10\.00", content)

    assert trace_match is not None, f"Expected 'Trace: 70.00' in {output_path}, but got:\n{content}"
    assert topleft_match is not None, f"Expected 'TopLeft: 10.00' in {output_path}, but got:\n{content}"