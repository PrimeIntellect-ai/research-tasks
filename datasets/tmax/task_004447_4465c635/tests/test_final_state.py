# test_final_state.py

import os
import subprocess
import pytest

def test_fix_summary_exists():
    path = "/home/user/fix_summary.txt"
    assert os.path.isfile(path), f"The file {path} is missing. Did you create it?"

    with open(path, "r") as f:
        content = f.read().strip()

    assert len(content) > 10, f"The file {path} seems empty or too short. Please provide a brief explanation of both fixes."

def test_make_test_passes():
    cwd = "/home/user/log_service"
    assert os.path.isdir(cwd), f"Directory {cwd} is missing."

    # Recompile to ensure the binary is up to date with logd.c
    compile_result = subprocess.run(
        ["make"],
        cwd=cwd,
        capture_output=True,
        text=True
    )
    assert compile_result.returncode == 0, f"Compilation failed:\n{compile_result.stderr}"

    # Run tests with a timeout to catch deadlocks
    try:
        test_result = subprocess.run(
            ["make", "test"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=15
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Running 'make test' timed out. The deadlock issue is likely not fixed.")

    assert test_result.returncode == 0, (
        f"'make test' failed. The parser bug or deadlock might not be fully fixed.\n"
        f"STDOUT:\n{test_result.stdout}\n"
        f"STDERR:\n{test_result.stderr}"
    )

def test_logd_c_modified():
    path = "/home/user/log_service/logd.c"
    assert os.path.isfile(path), f"{path} is missing."

    with open(path, "r") as f:
        content = f.read()

    # Heuristic: ensure there's an unlock call in the file (specifically, we expect it to be used correctly now)
    assert "pthread_mutex_unlock" in content, "Could not find 'pthread_mutex_unlock' in logd.c. The deadlock fix requires unlocking the mutex."