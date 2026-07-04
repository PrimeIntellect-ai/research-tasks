# test_final_state.py

import os
import subprocess
import pytest

BASE_DIR = "/home/user/ticket_8821/stat_calc"
RESOLUTION_FILE = "/home/user/ticket_8821/resolution.txt"

def test_resolution_file():
    assert os.path.isfile(RESOLUTION_FILE), f"{RESOLUTION_FILE} is missing."
    with open(RESOLUTION_FILE, "r") as f:
        content = f.read().strip()
    assert content == "RESOLVED", f"Expected 'RESOLVED' in {RESOLUTION_FILE}, but got '{content}'"

def test_run_tests_sh_passes():
    run_tests_sh = os.path.join(BASE_DIR, "run_tests.sh")
    assert os.path.isfile(run_tests_sh), f"{run_tests_sh} is missing."

    # Check that it doesn't contain the old bad path
    with open(run_tests_sh, "r") as f:
        content = f.read()
    assert "/tmp/nonexistent_config_12345.toml" not in content, "run_tests.sh still contains the misconfigured path."

    # Run the script and ensure it succeeds
    result = subprocess.run(["bash", run_tests_sh], cwd=BASE_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"run_tests.sh failed.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_regression_test_exists_and_content():
    regression_test = os.path.join(BASE_DIR, "tests", "regression_test.rs")
    assert os.path.isfile(regression_test), f"{regression_test} is missing."

    with open(regression_test, "r") as f:
        content = f.read()

    assert "100000.0" in content and "100000.1" in content and "100000.2" in content, \
        "regression_test.rs does not contain the required test data [100000.0, 100000.1, 100000.2]."
    assert "calculate_variance" in content, "regression_test.rs does not call calculate_variance."
    assert "0.00666" in content or "0.00667" in content or "6.66" in content, \
        "regression_test.rs does not contain the expected variance value (approx 0.006666)."

def test_cargo_test_passes():
    # Run cargo test directly with the correct env var to ensure tests pass
    env = os.environ.copy()
    env["STAT_CONFIG_PATH"] = os.path.join(BASE_DIR, "config.toml")
    result = subprocess.run(["cargo", "test"], cwd=BASE_DIR, env=env, capture_output=True, text=True)
    assert result.returncode == 0, f"cargo test failed.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

    # Check if regression_test was actually run
    assert "regression_test" in result.stdout or "regression" in result.stdout, \
        "regression_test was not executed during cargo test."