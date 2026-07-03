# test_final_state.py

import os
import pytest

def test_c_program_exists():
    """Verify that the C source file and compiled executable exist."""
    source_file = "/home/user/audit_path.c"
    executable = "/home/user/audit_path"

    assert os.path.exists(source_file), f"Missing C source file: {source_file}"
    assert os.path.isfile(source_file), f"Path is not a file: {source_file}"

    assert os.path.exists(executable), f"Missing compiled executable: {executable}"
    assert os.path.isfile(executable), f"Path is not a file: {executable}"
    assert os.access(executable, os.X_OK), f"File is not executable: {executable}"

def test_shortest_path_output():
    """Verify the shortest path output file contains the correct path."""
    path_file = "/home/user/shortest_path.txt"

    assert os.path.exists(path_file), f"Missing output file: {path_file}"
    assert os.path.isfile(path_file), f"Path is not a file: {path_file}"

    with open(path_file, "r") as f:
        content = f.read().strip()

    expected_path = "ENTRY_PORTAL,PROXY_B,CACHE_SERVER,DB_RELAY,SECURE_VAULT"
    assert content == expected_path, f"Incorrect shortest path. Expected '{expected_path}', got '{content}'"

def test_total_weight_output():
    """Verify the total weight output file contains the correct weight."""
    weight_file = "/home/user/total_weight.txt"

    assert os.path.exists(weight_file), f"Missing output file: {weight_file}"
    assert os.path.isfile(weight_file), f"Path is not a file: {weight_file}"

    with open(weight_file, "r") as f:
        content = f.read().strip()

    expected_weight = "28"
    assert content == expected_weight, f"Incorrect total weight. Expected '{expected_weight}', got '{content}'"