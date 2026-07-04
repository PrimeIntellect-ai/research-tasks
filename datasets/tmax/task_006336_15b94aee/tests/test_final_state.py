# test_final_state.py
import os
import subprocess
import pytest

def test_firewall_log_contents():
    log_path = "/home/user/firewall.log"
    assert os.path.exists(log_path), f"Firewall log was not created at {log_path}"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 1, f"Expected exactly 1 blocked request in firewall.log, but found {len(lines)}."
    assert lines[0] == "BLOCKED: 192.168.1.99", f"Expected 'BLOCKED: 192.168.1.99' in firewall.log, got '{lines[0]}'."

def test_traffic_log_contents():
    log_path = "/home/user/traffic.log"
    assert os.path.exists(log_path), f"Traffic log was not created at {log_path}"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = {
        "[192.168.1.10] [malicious.sh] The user purchased an item with CC: XXXX-XXXX-XXXX-XXXX today.",
        "[10.0.0.5] [cmd.exe] Valid payload without CC."
    }

    assert len(lines) == 2, f"Expected exactly 2 processed requests in traffic.log, but found {len(lines)}."

    actual_lines_set = set(lines)
    missing = expected_lines - actual_lines_set
    unexpected = actual_lines_set - expected_lines

    assert actual_lines_set == expected_lines, (
        f"Traffic log contents are incorrect.\n"
        f"Missing expected lines: {missing}\n"
        f"Unexpected lines found: {unexpected}"
    )

def test_encrypted_payloads():
    uploads_dir = "/home/user/uploads"
    assert os.path.isdir(uploads_dir), f"Uploads directory does not exist at {uploads_dir}"

    expected_files = {
        "malicious.sh.enc": "The user purchased an item with CC: XXXX-XXXX-XXXX-XXXX today.",
        "cmd.exe.enc": "Valid payload without CC."
    }

    # K = 'K'*32 -> hex is 4B repeated 32 times
    key_hex = "4B" * 32
    # IV = 'V'*16 -> hex is 56 repeated 16 times
    iv_hex = "56" * 16

    for fname, expected_text in expected_files.items():
        fpath = os.path.join(uploads_dir, fname)
        assert os.path.exists(fpath), f"Expected encrypted file {fpath} was not found. Check path traversal prevention and file naming."

        # Verify encryption using OpenSSL CLI
        cmd = [
            "openssl", "enc", "-aes-256-cbc", "-d",
            "-in", fpath,
            "-K", key_hex,
            "-iv", iv_hex
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        assert result.returncode == 0, (
            f"Failed to decrypt {fname}. Ensure it was encrypted with AES-256-CBC, "
            f"key='K'*32, iv='V'*16.\nOpenSSL Error: {result.stderr}"
        )

        decrypted_text = result.stdout
        assert decrypted_text == expected_text, (
            f"Decrypted content for {fname} does not match expected text.\n"
            f"Expected: {expected_text}\n"
            f"Got: {decrypted_text}\n"
            f"Ensure redaction happens BEFORE encryption."
        )