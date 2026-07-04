# test_final_state.py
import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_ci_success_log_exists():
    """Verify that the user actually ran ci.sh and it succeeded."""
    log_path = os.path.join(PROJECT_DIR, "ci_success.log")
    assert os.path.isfile(log_path), f"Expected {log_path} to exist. Did you run ci.sh?"

    with open(log_path, "r") as f:
        content = f.read().strip()
    assert content == "SUCCESS", f"Expected ci_success.log to contain 'SUCCESS', got '{content}'."

def test_processor_c_fixed_and_tests_pass():
    """Recompile the C code and run the tests to ensure the bug is actually fixed."""
    so_path = os.path.join(PROJECT_DIR, "libprocessor.so")
    if os.path.exists(so_path):
        os.remove(so_path)

    # Recompile the library
    make_result = subprocess.run(
        ["make"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert make_result.returncode == 0, f"Compilation failed:\n{make_result.stderr}"

    # Run the tests
    test_result = subprocess.run(
        ["python3", "tests/run_all.py"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )

    # If the bug is not fixed, this will segfault (returncode != 0)
    assert test_result.returncode == 0, (
        f"Tests failed (likely a segmentation fault). The bug in memory management "
        f"is not completely fixed.\nOutput:\n{test_result.stdout}\n{test_result.stderr}"
    )