# test_final_state.py
import os
import json
import pytest

def test_audit_py_exists():
    """Verify that the audit script was created."""
    script_path = "/home/user/audit.py"
    assert os.path.isfile(script_path), f"Expected script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()
        assert "pymongo" in content, "Script does not seem to import or use pymongo."
        assert "networkx" in content, "Script does not seem to import or use networkx."

def test_audit_results_json():
    """Verify that the audit results JSON was generated and contains the correct output."""
    results_path = "/home/user/audit_results.json"
    assert os.path.isfile(results_path), f"Expected output file {results_path} does not exist."

    with open(results_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} is not valid JSON.")

    expected_users = ["admin_01", "emp_02", "emp_03", "emp_05"]

    assert isinstance(data, list), "Output JSON should be a list of strings."
    assert data == expected_users, f"Expected {expected_users}, but got {data}."