# test_final_state.py

import os
import pytest

WORKSPACE_DIR = "/home/user/workspace"

def test_libdecoder_compiled():
    lib_path = os.path.join(WORKSPACE_DIR, "libdecoder.so")
    assert os.path.exists(lib_path), f"Shared library {lib_path} was not compiled."
    assert os.path.isfile(lib_path), f"{lib_path} is not a file."

def test_sorter_compiled():
    sorter_path = os.path.join(WORKSPACE_DIR, "sorter")
    assert os.path.exists(sorter_path), f"Executable {sorter_path} was not compiled."
    assert os.path.isfile(sorter_path), f"{sorter_path} is not a file."
    assert os.access(sorter_path, os.X_OK), f"{sorter_path} is not executable."

def test_integration_test_script_exists():
    script_path = os.path.join(WORKSPACE_DIR, "integration_test.py")
    assert os.path.exists(script_path), f"Python script {script_path} was not created."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_result_log_exists_and_content():
    log_path = os.path.join(WORKSPACE_DIR, "test_result.log")
    assert os.path.exists(log_path), f"Result log {log_path} was not created."
    assert os.path.isfile(log_path), f"{log_path} is not a file."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert len(content) > 0, f"{log_path} is empty."
    # The instructions state to write PASS if no diff, or the diff otherwise.
    # We just assert it wrote something since the exact diff output can vary depending on diff tool used.