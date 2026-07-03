# test_final_state.py

import os
import hashlib
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/process_backup.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_quarantine_log():
    log_path = "/home/user/quarantine.log"
    assert os.path.isfile(log_path), f"Quarantine log {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_malicious = [
        "../../../etc/shadow",
        "/var/log/syslog"
    ]

    assert lines == expected_malicious, f"Quarantine log contents incorrect. Expected {expected_malicious}, got {lines}."

def test_safe_extracted_files():
    base_dir = "/home/user/safe_restore"

    expected_files = {
        "system/info.txt": b"System is operational.\n",
        "web/index.html": b"<html>Hello</html>\n",
        "deep/nested/dir/config.json": b'{"key": "value"}\n',
        "safe_but_tricky..txt": b'".." is not "../"\n'
    }

    for rel_path, expected_content in expected_files.items():
        full_path = os.path.join(base_dir, rel_path)
        assert os.path.isfile(full_path), f"Expected extracted file {full_path} does not exist."

        with open(full_path, "rb") as f:
            content = f.read()

        assert content == expected_content, f"Content of {full_path} is incorrect."

def test_restore_checksums():
    checksum_path = "/home/user/restore_checksums.txt"
    assert os.path.isfile(checksum_path), f"Checksum manifest {checksum_path} does not exist."

    expected_files = {
        "system/info.txt": b"System is operational.\n",
        "web/index.html": b"<html>Hello</html>\n",
        "deep/nested/dir/config.json": b'{"key": "value"}\n',
        "safe_but_tricky..txt": b'".." is not "../"\n'
    }

    expected_lines = []
    for rel_path, content in expected_files.items():
        sha256 = hashlib.sha256(content).hexdigest()
        expected_lines.append(f"{sha256}  {rel_path}")

    expected_lines.sort()

    with open(checksum_path, "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_lines == expected_lines, "Checksum manifest contents or sorting are incorrect."

def test_restore_status():
    status_path = "/home/user/restore_status.txt"
    assert os.path.isfile(status_path), f"Status file {status_path} does not exist."

    with open(status_path, "r") as f:
        content = f.read().strip()

    assert content == "EXTRACTION COMPLETE", f"Status file content incorrect. Expected 'EXTRACTION COMPLETE', got '{content}'."