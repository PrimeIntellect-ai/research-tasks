# test_final_state.py

import os
import subprocess
import re
import hashlib

def test_phase1_upload_handler_patched():
    script_path = "/home/user/upload_handler.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing"

    # Test path traversal payload
    result = subprocess.run(
        [script_path, "../../etc/passwd", "dummy.txt"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 1, f"Expected script to exit with 1, got {result.returncode}"
    assert "Invalid filename" in result.stdout, "Expected 'Invalid filename' in stdout"

def test_phase1_audit_log():
    log_path = "/home/user/audit.log"
    assert os.path.isfile(log_path), f"Audit log {log_path} is missing"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "CWE-22 detected and patched", f"Audit log content incorrect: {content}"

def test_phase2_file_integrity():
    uploads_dir = "/home/user/uploads"
    quarantine_dir = "/home/user/quarantine"

    assert os.path.isdir(uploads_dir), f"Directory {uploads_dir} is missing"
    assert os.path.isdir(quarantine_dir), f"Directory {quarantine_dir} is missing"

    uploads_files = set(os.listdir(uploads_dir))
    quarantine_files = set(os.listdir(quarantine_dir))

    expected_uploads = {"file1.txt", "file2.txt"}
    expected_quarantine = {"file3.txt", "bad_actor.sh"}

    assert uploads_files == expected_uploads, f"Uploads directory should only contain {expected_uploads}, found {uploads_files}"
    assert expected_quarantine.issubset(quarantine_files), f"Quarantine directory is missing some expected files. Found {quarantine_files}"

def test_phase3_tokens():
    secret_path = "/home/user/new_tokens_secret.txt"
    hashes_path = "/home/user/valid_tokens.txt"

    assert os.path.isfile(secret_path), f"File {secret_path} is missing"
    assert os.path.isfile(hashes_path), f"File {hashes_path} is missing"

    with open(secret_path, "r") as f:
        secrets = [line.strip() for line in f if line.strip()]

    with open(hashes_path, "r") as f:
        hashes = [line.strip() for line in f if line.strip()]

    assert len(secrets) == 5, f"Expected exactly 5 tokens in {secret_path}, found {len(secrets)}"
    assert len(hashes) == 5, f"Expected exactly 5 hashes in {hashes_path}, found {len(hashes)}"

    token_pattern = re.compile(r"^[a-zA-Z0-9]{32}$")

    for i in range(5):
        secret = secrets[i]
        assert token_pattern.match(secret), f"Token '{secret}' is not a 32-character alphanumeric string"

        expected_hash = hashlib.sha256(secret.encode('utf-8')).hexdigest()
        actual_hash_line = hashes[i]

        # Extract the hash part from the line (e.g., "hash  -")
        actual_hash = actual_hash_line.split()[0]

        assert expected_hash == actual_hash, f"Hash mismatch at line {i+1}. Expected {expected_hash}, found {actual_hash}"

def test_phase4_network_rules():
    rules_path = "/home/user/network_rules.conf"
    assert os.path.isfile(rules_path), f"File {rules_path} is missing"

    with open(rules_path, "r") as f:
        content = f.read()

    assert "DENY 198.51.100.42" in content, f"Expected rule 'DENY 198.51.100.42' not found in {rules_path}"