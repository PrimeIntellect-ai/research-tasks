# test_final_state.py
import os
import re

def test_compute_jsd_c_modified():
    file_path = "/home/user/compute_jsd.c"
    assert os.path.exists(file_path), f"{file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read()

    assert re.search(r'#pragma\s+omp\s+parallel\s+for\s+reduction', content), \
        f"{file_path} does not contain the required OpenMP parallel for reduction pragmas."

def test_compute_jsd_executable():
    file_path = "/home/user/compute_jsd"
    assert os.path.exists(file_path), f"{file_path} executable is missing."
    assert os.access(file_path, os.X_OK), f"{file_path} is not executable."

def test_jsd_output():
    file_path = "/home/user/jsd_output.txt"
    assert os.path.exists(file_path), f"{file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == "0.113271", f"Expected JSD output 0.113271, got '{content}'"

def test_profile_script():
    file_path = "/home/user/profile.sh"
    assert os.path.exists(file_path), f"{file_path} is missing."
    assert os.access(file_path, os.X_OK), f"{file_path} is not executable."

def test_times_txt():
    file_path = "/home/user/times.txt"
    assert os.path.exists(file_path), f"{file_path} is missing."

    with open(file_path, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 3, f"{file_path} should contain exactly 3 lines, found {len(lines)}."

    for i, line in enumerate(lines):
        try:
            float(line)
        except ValueError:
            assert False, f"Line {i+1} in {file_path} is not a valid floating-point number: '{line}'"