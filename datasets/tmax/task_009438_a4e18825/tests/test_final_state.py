# test_final_state.py

import os
import subprocess
import pytest

def test_cert_cn_file():
    cert_cn_path = "/home/user/cert_cn.txt"
    assert os.path.isfile(cert_cn_path), f"File {cert_cn_path} does not exist."
    with open(cert_cn_path, "r") as f:
        content = f.read().strip()
    assert content == "secure-upload.local", f"Expected 'secure-upload.local', but got '{content}' in {cert_cn_path}."

def test_cwe_file():
    cwe_path = "/home/user/cwe.txt"
    assert os.path.isfile(cwe_path), f"File {cwe_path} does not exist."
    with open(cwe_path, "r") as f:
        content = f.read().strip()
    assert content in ["CWE-22", "CWE-022"], f"Expected 'CWE-22', but got '{content}' in {cwe_path}."

def test_upload_handler_patched_traversal():
    script_path = "/home/user/upload_handler.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Test with path traversal payload
    payload = b"UPLOAD ../../../etc/passwd\n"
    process = subprocess.run(
        [script_path],
        input=payload,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout_output = process.stdout.decode('utf-8').strip()
    assert process.returncode == 1, f"Expected exit code 1 for path traversal, got {process.returncode}."
    assert "INVALID" in stdout_output, f"Expected 'INVALID' in stdout for path traversal, got '{stdout_output}'."

def test_upload_handler_patched_exact_dotdot():
    script_path = "/home/user/upload_handler.sh"

    # Test with exact ".." payload
    payload = b"UPLOAD ..\n"
    process = subprocess.run(
        [script_path],
        input=payload,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout_output = process.stdout.decode('utf-8').strip()
    assert process.returncode == 1, f"Expected exit code 1 for '..', got {process.returncode}."
    assert "INVALID" in stdout_output, f"Expected 'INVALID' in stdout for '..', got '{stdout_output}'."

def test_upload_handler_legitimate():
    script_path = "/home/user/upload_handler.sh"

    # Test with legitimate payload
    payload = b"UPLOAD legitimate.txt\n"
    process = subprocess.run(
        [script_path],
        input=payload,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout_output = process.stdout.decode('utf-8').strip()
    assert process.returncode == 0, f"Expected exit code 0 for legitimate file, got {process.returncode}."
    expected_output = "Saving to /home/user/uploads/legitimate.txt"
    assert expected_output in stdout_output, f"Expected '{expected_output}' in stdout, got '{stdout_output}'."