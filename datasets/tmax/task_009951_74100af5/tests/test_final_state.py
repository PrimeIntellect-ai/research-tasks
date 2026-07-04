# test_final_state.py
import os
import subprocess
import re

def test_algo_c_fixed():
    path = "/home/user/numeric-lib/algo.c"
    assert os.path.isfile(path), f"File {path} does not exist"

    with open(path, "r") as f:
        content = f.read()

    # The bug was `static double cache[3];` which causes a race condition.
    # It should be removed, or changed to a local variable or thread-local.
    assert "static double cache" not in content, "The 'static double cache' shared state is still present in algo.c"

def test_go_test_race_passes():
    path = "/home/user/numeric-lib"
    assert os.path.isdir(path), f"Directory {path} does not exist"

    # Run go test -race
    result = subprocess.run(
        ["go", "test", "-race"],
        cwd=path,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"go test -race failed with output:\n{result.stdout}\n{result.stderr}"
    assert "WARNING: DATA RACE" not in result.stdout, "Data race still detected in go test output"
    assert "WARNING: DATA RACE" not in result.stderr, "Data race still detected in go test stderr"

def test_test_results_log_exists_and_correct():
    log_path = "/home/user/test_results.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist"

    with open(log_path, "r") as f:
        content = f.read()

    # Check that it contains something like "ok      numeric-lib"
    assert re.search(r"ok\s+numeric-lib", content) is not None, f"Expected passing test output in {log_path}, but got:\n{content}"
    assert "WARNING: DATA RACE" not in content, f"Data race warning found in {log_path}"