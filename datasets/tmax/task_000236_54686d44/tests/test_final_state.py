# test_final_state.py

import os
import stat
import string
import subprocess
import time
from pathlib import Path

def test_vault_extracted():
    """Verify that the original vault was decrypted and extracted."""
    payload_path = Path("/home/user/vault/payload.elf")
    assert payload_path.exists(), f"Missing extracted payload: {payload_path}. Did you extract the vault to /home/user/vault/?"
    assert payload_path.is_file(), f"Expected {payload_path} to be a file."

def test_new_key_created_and_permissions():
    """Verify the new key file exists, is 32-char alphanumeric, and has 0400 permissions."""
    key_path = Path("/home/user/new_key.txt")
    assert key_path.exists(), f"Missing new key file: {key_path}"

    with open(key_path, "r") as f:
        key = f.read().strip()

    assert len(key) == 32, f"New key length must be exactly 32 characters, got {len(key)}"
    assert all(c in string.ascii_letters + string.digits for c in key), "New key must be strictly alphanumeric."

    st = os.stat(key_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o400, f"Permissions of {key_path} must be exactly 0400, got {oct(perms)}"

def test_vault_reencrypted():
    """Verify the vault was re-encrypted with the new key and correct parameters."""
    new_vault_enc = Path("/home/user/vault_new.enc")
    key_path = Path("/home/user/new_key.txt")
    assert new_vault_enc.exists(), f"Missing re-encrypted vault: {new_vault_enc}"

    with open(key_path, "r") as f:
        key = f.read().strip()

    decrypted_zip = "/tmp/test_decrypted.zip"
    cmd = [
        "openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2", 
        "-in", str(new_vault_enc), 
        "-out", decrypted_zip, 
        "-pass", f"pass:{key}"
    ]
    res = subprocess.run(cmd, capture_output=True)
    assert res.returncode == 0, f"Failed to decrypt vault_new.enc with the new key. stderr: {res.stderr.decode()}"
    assert os.path.exists(decrypted_zip), "Decrypted archive was not created."

def test_ids_scanner_performance_and_correctness():
    """Verify the IDS scanner correctly identifies the signature and meets the performance threshold."""
    scanner_path = Path("/home/user/ids_scanner.py")
    input_log = Path("/app/test_logs.txt")
    output_log = Path("/tmp/detected.log")

    assert scanner_path.exists(), f"Missing scanner script: {scanner_path}"
    assert input_log.exists(), f"Missing input test logs: {input_log}"

    # Run the scanner and measure execution time
    start = time.time()
    res = subprocess.run(["python3", str(scanner_path), str(input_log), str(output_log)], capture_output=True)
    duration = time.time() - start

    assert res.returncode == 0, f"Scanner failed to run. stderr: {res.stderr.decode()}"
    assert output_log.exists(), "Scanner did not create the output log file."

    # Compute the expected lines based on the signature
    # Signature: DE AD BE EF 11 22 33 44 55 66 77 88
    sig = "deadbeef1122334455667788"

    expected_lines = []
    with open(input_log, "r") as f:
        for line in f:
            if sig in line.replace(" ", "").lower():
                expected_lines.append(line)

    with open(output_log, "r") as f:
        actual_lines = f.readlines()

    assert len(actual_lines) == len(expected_lines), f"Scanner output has {len(actual_lines)} lines, expected {len(expected_lines)}."
    assert actual_lines == expected_lines, "Output log lines do not match the expected lines containing the signature."

    # Assert performance threshold
    threshold = 0.75
    assert duration <= threshold, f"Execution time {duration:.3f}s exceeded threshold of {threshold}s"