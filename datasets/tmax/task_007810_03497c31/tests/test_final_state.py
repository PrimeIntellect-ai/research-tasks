# test_final_state.py

import os
import pytest

def test_safe_artifacts_extracted():
    safe1_path = "/home/user/safe_artifacts/safe1.bin"
    safe2_path = "/home/user/safe_artifacts/safe2.bin"

    assert os.path.exists(safe1_path), f"Safe artifact {safe1_path} was not extracted."
    with open(safe1_path, "rb") as f:
        assert f.read() == b"safe data 1\n", f"Content of {safe1_path} is incorrect."

    assert os.path.exists(safe2_path), f"Safe artifact {safe2_path} was not extracted."
    with open(safe2_path, "rb") as f:
        assert f.read() == b"safe data 2\n", f"Content of {safe2_path} is incorrect."

def test_malicious_artifacts_quarantined():
    mal1_path = "/home/user/quarantine/1.bin"
    mal2_path = "/home/user/quarantine/3.bin"

    assert os.path.exists(mal1_path), f"Malicious artifact was not quarantined at {mal1_path}."
    with open(mal1_path, "rb") as f:
        assert f.read() == b"malicious data A\n", f"Content of {mal1_path} is incorrect."

    assert os.path.exists(mal2_path), f"Malicious artifact was not quarantined at {mal2_path}."
    with open(mal2_path, "rb") as f:
        assert f.read() == b"malicious data B\n", f"Content of {mal2_path} is incorrect."

def test_quarantine_log():
    log_path = "/home/user/quarantine.log"
    assert os.path.exists(log_path), f"Quarantine log {log_path} is missing."

    with open(log_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "../escape.bin",
        "/etc/fake_shadow"
    ]

    assert lines == expected_lines, f"Quarantine log does not contain the expected entries. Found: {lines}"

def test_cpp_program_exists():
    cpp_path = "/home/user/curator.cpp"
    bin_path = "/home/user/curator"

    assert os.path.exists(cpp_path), f"C++ source file {cpp_path} does not exist."
    assert os.path.exists(bin_path), f"Compiled binary {bin_path} does not exist."
    assert os.access(bin_path, os.X_OK), f"Compiled binary {bin_path} is not executable."