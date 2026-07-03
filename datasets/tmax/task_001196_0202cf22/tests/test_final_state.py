# test_final_state.py

import os
import stat
import json
import pytest

def test_deploy_script_exists_and_executable():
    """Check if deploy.sh exists and has executable permissions."""
    path = "/home/user/deploy.sh"
    assert os.path.exists(path), f"File {path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."

def test_config_file_correct():
    """Check if the config file was created and formatted correctly."""
    path = "/home/user/config/site_users.ini"
    assert os.path.exists(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) > 0, f"File {path} is empty."
    assert lines[0] == "[Users]", f"First line of {path} is not exactly '[Users]'."

    expected_entries = {"alice=editor", "bob=viewer", "charlie=admin"}
    actual_entries = set(lines[1:])

    for entry in expected_entries:
        assert entry in actual_entries, f"Expected entry '{entry}' not found in {path}."

def test_archive_directory_correct():
    """Check if the archive directory exists and contains the processed files."""
    archive_dir = "/home/user/archive"
    assert os.path.isdir(archive_dir), f"Directory {archive_dir} does not exist."

    expected_files = ["alice.txt", "bob.txt", "charlie.txt"]
    for f in expected_files:
        filepath = os.path.join(archive_dir, f)
        assert os.path.exists(filepath), f"File {filepath} was not moved to the archive."

def test_requests_directory_empty():
    """Check if the processed files were removed from the requests directory."""
    requests_dir = "/home/user/requests"
    assert os.path.isdir(requests_dir), f"Directory {requests_dir} does not exist."

    expected_missing = ["alice.txt", "bob.txt", "charlie.txt"]
    for f in expected_missing:
        filepath = os.path.join(requests_dir, f)
        assert not os.path.exists(filepath), f"File {filepath} still exists in the requests directory."

def test_idp_received_log():
    """Check if the mock IdP received the correct JSON payloads."""
    log_path = "/home/user/idp_received.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist. Did the script successfully POST to the mock IdP through the SSH tunnel?"

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    parsed_logs = []
    for line in lines:
        try:
            parsed_logs.append(json.loads(line))
        except json.JSONDecodeError:
            pass

    expected_logs = [
        {"username": "alice", "role": "editor"},
        {"username": "bob", "role": "viewer"},
        {"username": "charlie", "role": "admin"}
    ]

    for expected in expected_logs:
        assert expected in parsed_logs, f"Expected JSON payload {expected} not found in {log_path}."