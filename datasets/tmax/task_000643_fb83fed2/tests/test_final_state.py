# test_final_state.py

import os
import subprocess
import pytest

def test_success_file_exists_and_content():
    path = "/home/user/success.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "ALL TESTS PASSED", f"Expected 'ALL TESTS PASSED', got '{content}'"

def test_makefile_fixed():
    path = "/home/user/stats/Makefile"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    # Check if STATS_ENV=test is present in the Makefile
    assert "STATS_ENV=test" in content, "Makefile does not set STATS_ENV=test for the test target."

def test_stats_go_fixed():
    path = "/home/user/stats/stats.go"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    # The buggy line was: z := (x - stddev) / mean
    # The correct line should be computing (x - mean) / stddev
    assert "(x - stddev) / mean" not in content, "stats.go still contains the buggy Z-score formula."
    assert "mean" in content and "stddev" in content, "stats.go seems to be missing required variables."

def test_make_test_passes():
    # Run the tests to ensure they actually pass
    try:
        result = subprocess.run(
            ["make", "test"],
            cwd="/home/user/stats",
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"'make test' failed with exit code {e.returncode}.\nStdout: {e.stdout}\nStderr: {e.stderr}")

    assert "ok" in result.stdout or "PASS" in result.stdout, "Test output does not indicate success."