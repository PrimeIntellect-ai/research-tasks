# test_final_state.py
import os
import subprocess
import pytest

def test_minimized_crash_txt():
    path = "/home/user/minimized_crash.txt"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert content == "[[[*", f"Expected minimized_crash.txt to contain exactly '[[[*', but got '{content}'"

def test_parser_fixed():
    binary_path = "/home/user/parser"
    assert os.path.isfile(binary_path), f"Binary {binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

    # Test that it no longer hangs on the minimal crash string
    try:
        result = subprocess.run([binary_path, "[[[*"], timeout=1, capture_output=True, text=True)
        assert result.returncode == 0 or result.returncode != 0, "Parser ran without hanging."
    except subprocess.TimeoutExpired:
        pytest.fail("The parser binary still hangs on the input '[[[*'. The loop termination bug was not correctly fixed.")

def test_test_runner_script():
    path = "/home/user/test_runner.sh"
    assert os.path.isfile(path), f"File {path} is missing."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_stats_log():
    path = "/home/user/stats.log"
    assert os.path.isfile(path), f"File {path} is missing. Did you run the test_runner.sh script?"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "Timeout Failures: 0", f"Expected stats.log to contain 'Timeout Failures: 0', but got '{content}'"