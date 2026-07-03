# test_final_state.py

import os
import json
import math
import pytest

def test_go_mod_exists_and_content():
    """Verify that the go.mod file exists and contains the correct module and dependency."""
    go_mod_path = "/home/user/polycalc/go.mod"
    assert os.path.exists(go_mod_path), f"File {go_mod_path} does not exist."

    with open(go_mod_path, 'r') as f:
        content = f.read()

    assert "module polycalc" in content, "go.mod does not contain 'module polycalc'."
    assert "github.com/gorilla/mux" in content, "go.mod does not require 'github.com/gorilla/mux'."

def test_bash_script_exists_and_executable():
    """Verify that the test script exists and is executable."""
    script_path = "/home/user/test_polycalc.sh"
    assert os.path.exists(script_path), f"File {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"File {script_path} is not executable."

def test_log_file_contents():
    """Verify that the log file contains the correct JSON responses."""
    log_path = "/home/user/integration_results.log"
    assert os.path.exists(log_path), f"File {log_path} does not exist."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) >= 2, f"Expected at least 2 lines of JSON in {log_path}, got {len(lines)}."

    # Parse first response
    try:
        resp1 = json.loads(lines[0])
    except json.JSONDecodeError:
        pytest.fail(f"First line of {log_path} is not valid JSON: {lines[0]}")

    assert resp1.get("lower") == 0, f"Expected lower=0, got {resp1.get('lower')}"
    assert resp1.get("upper") == 5, f"Expected upper=5, got {resp1.get('upper')}"
    assert resp1.get("steps") == 100, f"Expected steps=100, got {resp1.get('steps')}"

    result = resp1.get("result")
    assert result is not None, "First response missing 'result' field."
    assert math.isclose(result, 81.66666666666667, rel_tol=1e-5), f"Expected result ~81.66667, got {result}"

    # Parse second response
    try:
        resp2 = json.loads(lines[1])
    except json.JSONDecodeError:
        pytest.fail(f"Second line of {log_path} is not valid JSON: {lines[1]}")

    expected_error = "steps must be an even integer greater than 0"
    assert resp2.get("error") == expected_error, f"Expected error message '{expected_error}', got '{resp2.get('error')}'"