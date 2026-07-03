# test_final_state.py

import os
import pytest

def test_audit_server_script_exists_and_executable():
    """Test that the audit_server.sh script exists and is executable."""
    script_path = "/home/user/audit_server.sh"
    assert os.path.exists(script_path), f"Missing required script: {script_path}"
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_audit_results_content():
    """Test that the audit_results.txt file contains the correct findings."""
    results_path = "/home/user/audit_results.txt"
    assert os.path.exists(results_path), f"Missing required results file: {results_path}"
    assert os.path.isfile(results_path), f"{results_path} is not a file."

    expected_content = (
        "Endpoint: /api/v2/legacy_admin_auth\n"
        "Cookie: legacy_token\n"
        "CSP: Content-Security-Policy: default-src 'self'; script-src 'self';"
    )

    with open(results_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"Content of {results_path} does not match expected output.\n"
        f"Expected:\n{expected_content}\n\nActual:\n{actual_content}"
    )

def test_audit_server_script_contains_ulimit():
    """Test that the audit_server.sh script contains the required ulimit command."""
    script_path = "/home/user/audit_server.sh"
    if os.path.exists(script_path):
        with open(script_path, "r") as f:
            script_content = f.read()
        assert "ulimit -v 50000" in script_content, (
            f"The script {script_path} must set a strict virtual memory limit "
            "using 'ulimit -v 50000'."
        )