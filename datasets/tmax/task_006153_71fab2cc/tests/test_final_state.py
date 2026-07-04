# test_final_state.py

import os
import subprocess
import pytest

def test_invalid_sessions_enc_exists():
    """Check that the final encrypted file exists."""
    assert os.path.isfile("/home/user/invalid_sessions.enc"), (
        "The file /home/user/invalid_sessions.enc is missing. "
        "Did you forget to encrypt the results?"
    )

def test_invalid_sessions_enc_content():
    """Decrypt the results and verify the invalid sessions are correctly logged."""
    enc_path = "/home/user/invalid_sessions.enc"

    # Decrypt the file
    cmd = [
        "openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2",
        "-in", enc_path,
        "-pass", "pass:audit_pass_2024"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to decrypt /home/user/invalid_sessions.enc. "
                    f"Ensure it was encrypted with aes-256-cbc, -pbkdf2, and the correct password.\n"
                    f"OpenSSL error: {e.stderr}")

    decrypted_content = result.stdout.strip().splitlines()

    expected_lines = [
        "SESSION_ID: SESS-1002 | IP: 10.0.0.51",
        "SESSION_ID: SESS-1004 | IP: 192.168.1.105"
    ]

    assert len(decrypted_content) == len(expected_lines), (
        f"Expected {len(expected_lines)} lines in the decrypted log, "
        f"but found {len(decrypted_content)}."
    )

    for expected in expected_lines:
        assert expected in decrypted_content, (
            f"Expected line '{expected}' not found in the decrypted output. "
            f"Actual output:\n{result.stdout}"
        )