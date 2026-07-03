# test_final_state.py

import os
import subprocess
import pytest

def test_malicious_ips_file():
    ips_path = "/home/user/malicious_ips.txt"
    assert os.path.isfile(ips_path), f"File missing: {ips_path}"

    with open(ips_path, "r") as f:
        ips = [line.strip() for line in f if line.strip()]

    expected_ips = ["10.0.0.5", "203.0.113.42"]
    assert ips == expected_ips, f"Expected IPs {expected_ips}, but got {ips} in {ips_path}"

def test_block_rules_file():
    rules_path = "/home/user/block_rules.ipv4"
    assert os.path.isfile(rules_path), f"File missing: {rules_path}"

    with open(rules_path, "r") as f:
        rules = [line.strip() for line in f if line.strip()]

    expected_rules = [
        "-A INPUT -s 10.0.0.5 -j DROP",
        "-A INPUT -s 203.0.113.42 -j DROP"
    ]
    assert rules == expected_rules, f"Expected rules {expected_rules}, but got {rules} in {rules_path}"

def test_clean_uploads():
    clean_dir = "/home/user/clean_uploads"
    assert os.path.isdir(clean_dir), f"Directory missing: {clean_dir}"

    expected_files = {
        "file1.txt": "This is a clean file.\nIt has no malicious payloads.\n",
        "file4.txt": "Another clean file from this IP.\n"
    }

    for filename, expected_content in expected_files.items():
        file_path = os.path.join(clean_dir, filename)
        assert os.path.isfile(file_path), f"Clean file missing: {file_path}"
        with open(file_path, "r") as f:
            content = f.read()
        assert content == expected_content, f"Content mismatch in {file_path}"

def test_secure_vault_encryption():
    vault_dir = "/home/user/secure_vault"
    assert os.path.isdir(vault_dir), f"Directory missing: {vault_dir}"

    enc_file = os.path.join(vault_dir, "file3.txt.enc")
    assert os.path.isfile(enc_file), f"Encrypted file missing: {enc_file}"

    # Decrypt the file to verify
    decrypted_file = "/tmp/file3.txt.dec"
    cmd = [
        "openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2",
        "-pass", "pass:DevSecOps2024!",
        "-in", enc_file,
        "-out", decrypted_file
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Decryption failed: {result.stderr}"

    assert os.path.isfile(decrypted_file), "Decrypted file was not created"

    with open(decrypted_file, "r") as f:
        content = f.read()

    expected_content = "Here is my payment info.\nMy card is 1234567812345678.\nThanks!\n"
    assert content == expected_content, "Decrypted content does not match original"

    # Cleanup
    os.remove(decrypted_file)

def test_quarantine_is_empty():
    quarantine_dir = "/home/user/quarantine"
    assert os.path.isdir(quarantine_dir), f"Directory missing: {quarantine_dir}"

    files = os.listdir(quarantine_dir)
    assert len(files) == 0, f"Quarantine directory is not empty, found: {files}"