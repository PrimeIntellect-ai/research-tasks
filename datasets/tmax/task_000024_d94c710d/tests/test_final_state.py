# test_final_state.py

import os
import subprocess
import pytest

def test_secret_token_extracted():
    token_file = "/home/user/secret_token.txt"
    assert os.path.isfile(token_file), f"File {token_file} does not exist."

    with open(token_file, "r") as f:
        content = f.read().strip()

    assert content == "TKN-883A-29B1", f"Expected token 'TKN-883A-29B1', but got '{content}'."

def test_regression_test_file_exists():
    test_file = "/home/user/fast_profiler/tests/test_telemetry.c"
    assert os.path.isfile(test_file), f"File {test_file} does not exist."

    with open(test_file, "r") as f:
        content = f.read()

    assert "telemetry_init" in content, "test_telemetry.c does not contain 'telemetry_init'."
    assert "TELEMETRY_TOKEN" in content, "test_telemetry.c does not contain 'TELEMETRY_TOKEN'."

def test_build_succeeds():
    base_dir = "/home/user/fast_profiler"

    clean_result = subprocess.run(["make", "clean"], cwd=base_dir, capture_output=True, text=True)
    assert clean_result.returncode == 0, f"'make clean' failed:\n{clean_result.stderr}"

    build_result = subprocess.run(["make", "all"], cwd=base_dir, capture_output=True, text=True)
    assert build_result.returncode == 0, f"'make all' failed:\n{build_result.stderr}"

    assert os.path.isfile(os.path.join(base_dir, "libtelemetry.a")), "libtelemetry.a was not built."

def test_make_test_target():
    base_dir = "/home/user/fast_profiler"
    log_file = "/home/user/test_result.log"

    if os.path.exists(log_file):
        os.remove(log_file)

    test_result = subprocess.run(["make", "test"], cwd=base_dir, capture_output=True, text=True)
    assert test_result.returncode == 0, f"'make test' failed:\n{test_result.stderr}\n{test_result.stdout}"

    assert os.path.isfile(log_file), f"{log_file} was not created by 'make test'."

    with open(log_file, "r") as f:
        content = f.read().strip()

    assert content == "ALL TESTS PASSED", f"Expected 'ALL TESTS PASSED' in log file, but got '{content}'."