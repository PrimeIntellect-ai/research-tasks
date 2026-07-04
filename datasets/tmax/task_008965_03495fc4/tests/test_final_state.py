# test_final_state.py

import os
import json
import stat
import pytest
import subprocess

def test_audit_report_exists_and_valid():
    """Test that the audit_report.json exists and contains the correct data."""
    report_path = "/home/user/audit_report.json"
    assert os.path.isfile(report_path), f"Audit report not found at {report_path}"

    with open(report_path, "r") as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} does not contain valid JSON.")

    assert isinstance(report_data, list), "Audit report must be a JSON array."

    # Check sorting by filename
    filenames = [item.get("filename") for item in report_data]
    assert filenames == sorted(filenames), "Audit report must be sorted alphabetically by filename."

    # Map expected results
    expected_results = {
        "app1": False,
        "app2": True,
        "app3": False
    }

    found_files = {}
    for item in report_data:
        assert "filename" in item, "Missing 'filename' key in report item."
        assert "uses_insecure_gets" in item, "Missing 'uses_insecure_gets' key in report item."
        found_files[item["filename"]] = item["uses_insecure_gets"]

    for filename, expected_flag in expected_results.items():
        assert filename in found_files, f"File {filename} missing from audit report."
        assert found_files[filename] is expected_flag, f"Expected uses_insecure_gets for {filename} to be {expected_flag}, got {found_files[filename]}"

def test_sandbox_script_app2_exists_and_executable():
    """Test that the sandbox script for app2 is created correctly."""
    script_path = "/home/user/sandbox_app2.sh"
    assert os.path.isfile(script_path), f"Sandbox script not found at {script_path}"

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Sandbox script {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    assert "ulimit -c 0" in content, f"Sandbox script {script_path} must contain 'ulimit -c 0'."
    assert "env -i" in content, f"Sandbox script {script_path} must use 'env -i' to clear the environment."
    assert "app2" in content, f"Sandbox script {script_path} must execute the app2 binary."
    assert "$@" in content or "$*" in content, f"Sandbox script {script_path} must pass arguments to the binary."

def test_sandbox_scripts_not_created_for_safe_binaries():
    """Test that sandbox scripts are not created for safe binaries."""
    safe_scripts = [
        "/home/user/sandbox_app1.sh",
        "/home/user/sandbox_app3.sh"
    ]
    for script_path in safe_scripts:
        assert not os.path.exists(script_path), f"Sandbox script {script_path} should not exist for safe binaries."