# test_final_state.py

import os
import pytest

PROJECT_DIR = "/home/user/project"
PATCH_FILE = os.path.join(PROJECT_DIR, "Makefile.patch")
SCRIPT_FILE = os.path.join(PROJECT_DIR, "build_and_run.sh")
RESULT_FILE = "/home/user/result.txt"

def test_makefile_patch_exists():
    assert os.path.isfile(PATCH_FILE), f"Patch file '{PATCH_FILE}' does not exist."

def test_build_and_run_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_FILE), f"Script file '{SCRIPT_FILE}' does not exist."
    assert os.access(SCRIPT_FILE, os.X_OK), f"Script file '{SCRIPT_FILE}' is not executable."

def test_result_file_content():
    assert os.path.isfile(RESULT_FILE), f"Result file '{RESULT_FILE}' does not exist."

    with open(RESULT_FILE, "r") as f:
        content = f.read().strip()

    expected_content = "Result: 385"
    assert expected_content in content, f"Result file '{RESULT_FILE}' does not contain expected output. Found: '{content}'"