# test_final_state.py

import os
import re

def test_recovered_log():
    path = "/home/user/recovered.log"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    alloc_count = len(re.findall(r"^ALLOC\s+\d+\s+", content, re.MULTILINE))
    free_count = len(re.findall(r"^FREE\s+\d+\s+", content, re.MULTILINE))

    assert alloc_count == 50, f"Expected 50 ALLOC lines in {path}, found {alloc_count}."
    assert free_count == 43, f"Expected 43 FREE lines in {path}, found {free_count}."

def test_leaked_ids():
    path = "/home/user/leaked_ids.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        lines = f.read().strip().split('\n')

    ids = []
    for line in lines:
        if line.strip():
            try:
                ids.append(int(line.strip()))
            except ValueError:
                assert False, f"Non-integer value found in {path}: {line}"

    expected_ids = [7, 14, 21, 28, 35, 42, 49]
    assert ids == expected_ids, f"Expected leaked IDs {expected_ids}, but got {ids}."

def test_memory_tracker_c_fixed():
    path = "/home/user/memory_tracker.c"
    assert os.path.isfile(path), f"Source file {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "assert(" in content, f"Expected 'assert(' in {path}."
    assert "free(" in content, f"Expected 'free(' in {path}."

def test_memory_tracker_fixed_executable():
    path = "/home/user/memory_tracker_fixed"
    assert os.path.isfile(path), f"Executable {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."