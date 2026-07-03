# test_final_state.py

import os
import pytest

BASE_DIR = "/home/user/release_prep"

def test_merger_c_exists():
    filepath = os.path.join(BASE_DIR, "merger.c")
    assert os.path.isfile(filepath), f"{filepath} does not exist. The C source file is missing."

def test_merger_executable_exists():
    filepath = os.path.join(BASE_DIR, "merger")
    assert os.path.isfile(filepath), f"{filepath} does not exist. The C program was not compiled."
    assert os.access(filepath, os.X_OK), f"{filepath} is not executable."

def test_test_go_exists():
    filepath = os.path.join(BASE_DIR, "test.go")
    assert os.path.isfile(filepath), f"{filepath} does not exist. The Go test orchestrator is missing."

def test_status_txt_content():
    filepath = os.path.join(BASE_DIR, "status.txt")
    assert os.path.isfile(filepath), f"{filepath} does not exist. The Go program may not have run successfully."

    with open(filepath, "r") as f:
        content = f.read().strip()

    assert content == "ALL PASS", f"Expected 'ALL PASS' in {filepath}, but got '{content}'."