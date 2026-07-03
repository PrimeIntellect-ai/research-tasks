# test_final_state.py

import os
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/analyze_seq.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_script_no_forbidden_tools():
    script_path = "/home/user/analyze_seq.sh"
    if not os.path.isfile(script_path):
        pytest.skip(f"Script {script_path} does not exist.")

    with open(script_path, "r") as f:
        content = f.read()

    forbidden = ["python", "perl", "Rscript"]
    for tool in forbidden:
        assert tool not in content, f"Forbidden tool '{tool}' found in {script_path}. You must use standard CLI tools."

def test_regression_results():
    results_path = "/home/user/regression_results.txt"
    assert os.path.isfile(results_path), f"Output file {results_path} does not exist."

    with open(results_path, "r") as f:
        content = f.read().strip()

    expected = "Slope: 0.50\nIntercept: 35.00"
    assert content == expected, f"Contents of {results_path} do not match expected results. Got:\n{content}"

def test_test_log():
    log_path = "/home/user/test_log.txt"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "PASS", f"Contents of {log_path} are incorrect. Expected 'PASS', got '{content}'."