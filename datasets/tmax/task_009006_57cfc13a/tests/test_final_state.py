# test_final_state.py

import os
import stat
import pytest

def test_analyze_script_exists():
    path = "/home/user/analyze.py"
    assert os.path.isfile(path), f"Python script {path} does not exist."

def test_run_all_script_exists_and_executable():
    path = "/home/user/run_all.sh"
    assert os.path.isfile(path), f"Bash script {path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Bash script {path} is not executable."

def test_compiled_executable_exists():
    path = "/home/user/fasta_stat"
    assert os.path.isfile(path), f"Compiled executable {path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Compiled file {path} is not executable."

def test_result_txt_content():
    path = "/home/user/result.txt"
    assert os.path.isfile(path), f"Result file {path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, f"Result file {path} should contain at least 2 lines."

    # First line should be the integral value: 9.50
    assert lines[0] == "9.50", f"Expected first line to be '9.50', but got '{lines[0]}'."

    # Second line should be the output of the C program: Number of sequences: 1
    assert lines[1] == "Number of sequences: 1", f"Expected second line to be 'Number of sequences: 1', but got '{lines[1]}'."