# test_final_state.py

import os
import subprocess
import hashlib
import pytest

def test_audit_report():
    report_path = "/home/user/audit_report.txt"
    assert os.path.isfile(report_path), f"Audit report not found at {report_path}"

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().split('\n')]

    assert len(lines) >= 3, "Audit report must contain at least 3 lines"

    cwe_id = lines[0].upper()
    assert cwe_id == "CWE-22", f"Expected CWE-22 on line 1, got {lines[0]}"

    attacker_ip = lines[1]
    assert attacker_ip == "172.16.8.99", f"Expected attacker IP 172.16.8.99 on line 2, got {lines[1]}"

    # Calculate the hash of the malicious file dynamically
    malicious_file = "/home/user/secret_key.txt"
    assert os.path.isfile(malicious_file), f"Malicious file {malicious_file} is missing"

    with open(malicious_file, "rb") as mf:
        expected_hash = hashlib.sha256(mf.read()).hexdigest()

    file_hash = lines[2].lower()
    assert file_hash == expected_hash, f"Expected hash {expected_hash} on line 3, got {lines[2]}"

def test_patched_executable_exists():
    exe_path = "/home/user/upload_handler_patched"
    assert os.path.isfile(exe_path), f"Patched executable not found at {exe_path}"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable"

def test_patched_executable_valid_input():
    exe_path = "/home/user/upload_handler_patched"
    test_file = "valid_test_file.txt"
    test_content = "valid_data_123"

    # Ensure the upload directory exists
    os.makedirs("/home/user/uploads", exist_ok=True)

    # Run the executable from /home/user so relative path 'uploads/' works
    result = subprocess.run(
        [exe_path, test_file, test_content],
        cwd="/home/user",
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Expected exit code 0 for valid input, got {result.returncode}"

    output_file = f"/home/user/uploads/{test_file}"
    assert os.path.isfile(output_file), f"Expected file to be created at {output_file}"

    with open(output_file, "r") as f:
        content = f.read()
    assert content == test_content, f"Expected file content '{test_content}', got '{content}'"

def test_patched_executable_invalid_input_dotdot():
    exe_path = "/home/user/upload_handler_patched"

    result = subprocess.run(
        [exe_path, "../evil.txt", "data"],
        cwd="/home/user",
        capture_output=True,
        text=True
    )

    assert result.returncode == 1, f"Expected exit code 1 for input with '..', got {result.returncode}"
    assert "Invalid filename" in result.stderr, "Expected 'Invalid filename' in stderr"

def test_patched_executable_invalid_input_slash():
    exe_path = "/home/user/upload_handler_patched"

    result = subprocess.run(
        [exe_path, "/etc/passwd", "data"],
        cwd="/home/user",
        capture_output=True,
        text=True
    )

    assert result.returncode == 1, f"Expected exit code 1 for input with '/', got {result.returncode}"
    assert "Invalid filename" in result.stderr, "Expected 'Invalid filename' in stderr"