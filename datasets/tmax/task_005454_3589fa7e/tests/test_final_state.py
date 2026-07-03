# test_final_state.py

import os
import subprocess

def test_root_ca_extracted():
    """Verify that the root_ca.pem was extracted correctly."""
    root_ca_path = "/home/user/root_ca.pem"
    assert os.path.isfile(root_ca_path), f"Missing file: {root_ca_path}"

    with open(root_ca_path, "r") as f:
        content = f.read()
    assert "BEGIN CERTIFICATE" in content, f"File {root_ca_path} does not contain a valid PEM certificate."

def test_go_script_exists():
    """Verify that the Go script was created."""
    go_script_path = "/home/user/audit_verify.go"
    assert os.path.isfile(go_script_path), f"Missing file: {go_script_path}"

def test_compliance_result():
    """Verify the final compliance result file exists and has the correct content."""
    result_path = "/home/user/compliance_result.txt"
    assert os.path.isfile(result_path), f"Missing file: {result_path}"

    with open(result_path, "r") as f:
        content = f.read()

    expected_content = "STATUS: VALID - PAYLOAD: SECURE_AUDIT_998"
    assert content == expected_content, f"Expected content '{expected_content}', but got '{content}'"