# test_final_state.py

import os
import pytest

def test_app_binary_exists():
    app_path = "/home/user/ci_project/app"
    assert os.path.isfile(app_path), f"The binary {app_path} does not exist. Did you compile the project?"
    assert os.access(app_path, os.X_OK), f"The file {app_path} is not executable."

def test_output_log_exists():
    log_path = "/home/user/ci_project/output.log"
    assert os.path.isfile(log_path), f"The output log {log_path} does not exist. Did you run the compiled app?"

def test_output_log_contents():
    log_path = "/home/user/ci_project/output.log"
    assert os.path.isfile(log_path), f"The output log {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected = "TARGET=PROD\nUSER=ADMIN"

    assert content == expected, (
        f"The contents of {log_path} are incorrect or corrupted.\n"
        f"Expected:\n{expected}\n\nGot:\n{content}\n\n"
        "This indicates the memory lifetime issue was not properly fixed."
    )