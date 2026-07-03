# test_final_state.py
import os
import stat
import subprocess
import hashlib
import json
import base64
import pytest

def test_audit_report():
    report_path = "/home/user/audit_report.txt"
    assert os.path.isfile(report_path), f"Audit report not found at {report_path}"

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    assert len(lines) >= 3, "Audit report must contain exactly 3 lines."

    # Derive the malicious key from the payload to ensure truth alignment
    payload_path = "/home/user/evidence/payload.b64"
    assert os.path.isfile(payload_path), "Evidence payload missing."
    with open(payload_path, "r") as f:
        b64_data = f.read().strip()

    decoded_json = base64.b64decode(b64_data).decode('utf-8')
    payload = json.loads(decoded_json)
    malicious_key = payload.get("key", "")

    expected_cwe = "CWE-732"
    expected_hash = hashlib.sha256(malicious_key.encode('utf-8')).hexdigest()

    assert lines[0] == malicious_key, f"Line 1 of report is incorrect. Expected the malicious key."
    assert lines[1] == expected_cwe, f"Line 2 of report is incorrect. Expected {expected_cwe}."
    assert lines[2] == expected_hash, f"Line 3 of report is incorrect. Expected SHA256 hash of the malicious key."

def test_permissions():
    mock_ssh_dir = "/home/user/mock_ssh"
    auth_keys_file = "/home/user/mock_ssh/authorized_keys"

    assert os.path.isdir(mock_ssh_dir), f"{mock_ssh_dir} directory missing."
    assert os.path.isfile(auth_keys_file), f"{auth_keys_file} file missing."

    dir_stat = os.stat(mock_ssh_dir)
    assert stat.S_IMODE(dir_stat.st_mode) == 0o700, f"Permissions for {mock_ssh_dir} must be exactly 0700."

    file_stat = os.stat(auth_keys_file)
    assert stat.S_IMODE(file_stat.st_mode) == 0o600, f"Permissions for {auth_keys_file} must be exactly 0600."

def test_authorized_keys_content():
    auth_keys_file = "/home/user/mock_ssh/authorized_keys"
    valid_hashes_file = "/home/user/evidence/valid_hashes.txt"

    assert os.path.isfile(auth_keys_file), f"{auth_keys_file} file missing."
    assert os.path.isfile(valid_hashes_file), f"{valid_hashes_file} file missing."

    with open(valid_hashes_file, "r") as f:
        valid_hashes = set(line.strip() for line in f if line.strip())

    with open(auth_keys_file, "r") as f:
        keys = [line.strip() for line in f if line.strip()]

    assert len(keys) == len(valid_hashes), "The number of keys in authorized_keys does not match the number of valid hashes."

    for key in keys:
        key_hash = hashlib.sha256(key.encode('utf-8')).hexdigest()
        assert key_hash in valid_hashes, f"Found a key in authorized_keys that does not match any valid hash: {key}"

def test_rust_code_patch():
    main_rs_path = "/home/user/key_service/src/main.rs"
    assert os.path.isfile(main_rs_path), f"Rust source file missing at {main_rs_path}"

    with open(main_rs_path, "r") as f:
        content = f.read()

    assert "0o777" not in content, "The vulnerable 0o777 permission is still present in main.rs."
    assert "0o600" in content, "The secure 0o600 permission was not found in main.rs."
    assert "OpenOptionsExt" in content, "The code does not appear to use OpenOptionsExt to set permissions securely."

def test_rust_compilation():
    project_dir = "/home/user/key_service"
    assert os.path.isdir(project_dir), f"Rust project directory missing at {project_dir}"

    result = subprocess.run(
        ["cargo", "build"],
        cwd=project_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    assert result.returncode == 0, f"Rust project failed to compile:\n{result.stderr}"