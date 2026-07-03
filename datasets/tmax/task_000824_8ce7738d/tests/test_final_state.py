# test_final_state.py
import os
import stat
import pytest

def test_audit_log_contents():
    log_path = "/home/user/audit_log.txt"
    assert os.path.isfile(log_path), f"Audit log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "/home/user/uploads/backup/config.key",
        "/home/user/uploads/id_rsa_leaked"
    ]

    assert lines == expected_lines, f"Audit log contents are incorrect. Expected {expected_lines}, got {lines}"

def test_redacted_files():
    files_to_check = [
        ("/home/user/uploads/id_rsa_leaked", "-----BEGIN OPENSSH PRIVATE KEY-----\n[REDACTED]\n-----END OPENSSH PRIVATE KEY-----\n", 0o600),
        ("/home/user/uploads/backup/config.key", "Some config data here.\n-----BEGIN OPENSSH PRIVATE KEY-----\n[REDACTED]\n-----END OPENSSH PRIVATE KEY-----\nEnd of config data.\n", 0o600)
    ]

    for file_path, expected_content, expected_perm in files_to_check:
        assert os.path.isfile(file_path), f"File {file_path} does not exist."

        st = os.stat(file_path)
        assert stat.S_IMODE(st.st_mode) == expected_perm, f"Permissions for {file_path} should be {oct(expected_perm)}."

        with open(file_path, "r") as f:
            content = f.read()

        assert content == expected_content, f"Content for {file_path} is incorrect. Got:\n{content}"

def test_untouched_files():
    files_to_check = [
        ("/home/user/uploads/normal.txt", 0o644),
        ("/home/user/uploads/images/logo.png", 0o644)
    ]

    for file_path, expected_perm in files_to_check:
        assert os.path.isfile(file_path), f"File {file_path} does not exist."

        st = os.stat(file_path)
        assert stat.S_IMODE(st.st_mode) == expected_perm, f"Permissions for {file_path} should be {oct(expected_perm)}."

        if file_path == "/home/user/uploads/normal.txt":
            with open(file_path, "r") as f:
                content = f.read()
            assert "Just a normal text file uploaded by a user." in content, f"Content of {file_path} was altered."