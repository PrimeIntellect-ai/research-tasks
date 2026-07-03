# test_final_state.py

import os
import stat
import json
import subprocess
import pytest

def test_cwe_identification():
    script_path = "/home/user/app/cgi-bin/upload.sh"
    assert os.path.isfile(script_path), f"File missing: {script_path}"

    with open(script_path, "r") as f:
        lines = f.readlines()

    assert len(lines) >= 2, f"{script_path} does not have enough lines."
    assert lines[1].strip() == "# VULNERABILITY: CWE-22", (
        f"Line 2 of {script_path} must be exactly '# VULNERABILITY: CWE-22'. "
        f"Found: '{lines[1].strip()}'"
    )

def test_remediation():
    script_path = "/home/user/app/cgi-bin/upload.sh"
    assert os.path.isfile(script_path), f"File missing: {script_path}"

    with open(script_path, "r") as f:
        content = f.read()

    # Check if basename or ##*/ is used to sanitize the filename
    has_basename = "basename" in content
    has_param_expansion = "##*/" in content

    assert has_basename or has_param_expansion, (
        f"{script_path} does not contain 'basename' or '##*/' for path traversal remediation."
    )

def test_permissions():
    uploads_dir = "/home/user/app/uploads"
    assert os.path.isdir(uploads_dir), f"Directory missing: {uploads_dir}"

    dir_stat = os.stat(uploads_dir)
    dir_mode = oct(stat.S_IMODE(dir_stat.st_mode))
    assert dir_mode == "0o700", f"Directory {uploads_dir} must have 700 permissions, found {dir_mode}"

    for filename in os.listdir(uploads_dir):
        file_path = os.path.join(uploads_dir, filename)
        if os.path.isfile(file_path):
            file_stat = os.stat(file_path)
            file_mode = oct(stat.S_IMODE(file_stat.st_mode))
            assert file_mode == "0o600", f"File {file_path} must have 600 permissions, found {file_mode}"

def test_policy_script_exists_and_executable():
    script_path = "/home/user/check_policy.sh"
    assert os.path.isfile(script_path), f"Policy script missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Policy script {script_path} is not executable."

def test_policy_script_execution_and_output():
    script_path = "/home/user/check_policy.sh"
    json_path = "/home/user/policy_status.json"

    # Remove existing JSON if any to ensure the script creates it
    if os.path.exists(json_path):
        os.remove(json_path)

    # Execute the script
    try:
        subprocess.run([script_path], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {script_path} failed with error: {e.stderr}")

    assert os.path.isfile(json_path), f"JSON output missing: {json_path} was not created by the script."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} does not contain valid JSON.")

    expected_keys = {"cwe_identified", "port_8080_active", "uploads_dir_secure"}
    assert set(data.keys()) == expected_keys, f"JSON keys must be exactly {expected_keys}. Found: {set(data.keys())}"

    assert data["cwe_identified"] is True, "JSON field 'cwe_identified' must be true."
    assert data["port_8080_active"] is True, "JSON field 'port_8080_active' must be true."
    assert data["uploads_dir_secure"] is True, "JSON field 'uploads_dir_secure' must be true."