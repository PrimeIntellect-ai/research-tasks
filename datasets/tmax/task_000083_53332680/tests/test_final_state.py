# test_final_state.py

import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_result_log_correct():
    """Verify that the test_result.log exists and contains the correct output."""
    log_path = os.path.join(PROJECT_DIR, "test_result.log")
    assert os.path.isfile(log_path), f"The file {log_path} does not exist. Did you run the executable and redirect output?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected = "SUCCESS: Linked version 2.0.5"
    assert content == expected, f"Expected log content '{expected}', but got '{content}'"

def test_shared_library_built():
    """Verify that the shared library was built."""
    so_path = os.path.join(PROJECT_DIR, "libmathalg.so")
    assert os.path.isfile(so_path), f"Shared library {so_path} is missing. Did the Makefile build it?"

def test_executable_built():
    """Verify that the test_suite executable was built."""
    exe_path = os.path.join(PROJECT_DIR, "test_suite")
    assert os.path.isfile(exe_path), f"Executable {exe_path} is missing. Did the Makefile build it?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_executable_runs_independently():
    """Verify that the executable runs successfully without LD_LIBRARY_PATH (checking rpath)."""
    exe_path = os.path.join(PROJECT_DIR, "test_suite")
    assert os.path.isfile(exe_path), "test_suite executable not found."

    # Run the executable with a minimal environment to ensure it doesn't rely on LD_LIBRARY_PATH
    # and relies on the rpath compiled into it.
    try:
        result = subprocess.run(
            ["./test_suite"],
            cwd=PROJECT_DIR,
            env={"PATH": "/usr/bin:/bin"},  # Clear LD_LIBRARY_PATH
            capture_output=True,
            text=True,
            timeout=5
        )
    except Exception as e:
        pytest.fail(f"Failed to execute ./test_suite: {e}")

    assert result.returncode == 0, (
        f"test_suite failed to run independently. Return code: {result.returncode}\n"
        f"Stdout: {result.stdout}\nStderr: {result.stderr}\n"
        "Did you correctly set the rpath during linking?"
    )

    assert "SUCCESS: Linked version 2.0.5" in result.stdout, (
        f"test_suite output was incorrect when run independently.\nOutput: {result.stdout}"
    )