# test_final_state.py

import os
import stat
import pytest

def test_incident_report():
    path = "/home/user/incident_report.txt"
    assert os.path.exists(path), f"Missing required file: {path}"
    assert os.path.isfile(path), f"Path is not a file: {path}"

    with open(path, 'r') as f:
        content = f.read().strip()

    expected_content = "CWE: CWE-601\nSecret: Inc1d3nt_R3sp0nse_K3y_8872!"

    # Normalize line endings for comparison
    content_normalized = '\n'.join([line.strip() for line in content.splitlines() if line.strip()])
    expected_normalized = '\n'.join([line.strip() for line in expected_content.splitlines() if line.strip()])

    assert content_normalized == expected_normalized, f"Content of {path} is incorrect. Expected:\n{expected_content}\nGot:\n{content}"

def test_safe_token():
    path = "/home/user/safe_token.txt"
    assert os.path.exists(path), f"Missing required file: {path}"
    assert os.path.isfile(path), f"Path is not a file: {path}"

    with open(path, 'r') as f:
        content = f.read().strip()

    expected_token = "3187217578"
    assert content == expected_token, f"Content of {path} is incorrect. Expected {expected_token}, got {content}"

    # Check permissions
    st = os.stat(path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o600, f"Permissions of {path} are incorrect. Expected 0600, got {oct(perms)}"

def test_forge_cpp():
    path = "/home/user/forge.cpp"
    assert os.path.exists(path), f"Missing required file: {path}"
    assert os.path.isfile(path), f"Path is not a file: {path}"

    with open(path, 'r') as f:
        content = f.read()

    assert len(content.strip()) > 0, f"File {path} is empty"