# test_final_state.py

import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"
APP_PATH = os.path.join(PROJECT_DIR, "app")
LOG_PATH = os.path.join(PROJECT_DIR, "test_results.log")

def test_app_binary_exists_and_executable():
    assert os.path.isfile(APP_PATH), f"The compiled binary does not exist at {APP_PATH}"
    assert os.access(APP_PATH, os.X_OK), f"The file at {APP_PATH} is not executable"

def test_test_results_log_contains_passed():
    assert os.path.isfile(LOG_PATH), f"The log file does not exist at {LOG_PATH}"
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert "E2E TESTS PASSED" in content, f"The log file {LOG_PATH} does not contain 'E2E TESTS PASSED'"

def test_go_build_success():
    # Verify that the circular import is fixed by running go build
    result = subprocess.run(
        ["go", "build"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"'go build' failed in {PROJECT_DIR}. Output: {result.stderr}"