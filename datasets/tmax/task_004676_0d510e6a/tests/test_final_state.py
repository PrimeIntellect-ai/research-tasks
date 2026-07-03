# test_final_state.py

import os
import subprocess
import pytest

def test_audit_flag_generated():
    """
    Validates that Phase 1 was completed successfully by checking if the
    buffer overflow triggered the hidden function and created the audit flag.
    """
    flag_path = "/home/user/audit_flag.txt"
    assert os.path.exists(flag_path), "Phase 1 Failed: /home/user/audit_flag.txt does not exist. The exploit may not have executed the hidden function."

    with open(flag_path, "r") as f:
        content = f.read().strip()

    assert content == "COMPLIANCE_AUDIT_PASSED_XYZ123", f"Phase 1 Failed: /home/user/audit_flag.txt contains incorrect data: {content}"

def test_audit_trail_encrypted():
    """
    Validates Phase 2 by attempting to decrypt the audit_trail.enc file
    using the exact AES-256-CBC key and IV specified in the task.
    """
    enc_path = "/home/user/audit_trail.enc"
    assert os.path.exists(enc_path), "Phase 2 Failed: /home/user/audit_trail.enc does not exist."

    key = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
    iv = "00112233445566778899aabbccddeeff"

    # Use openssl to decrypt since Python stdlib lacks AES
    cmd = [
        "openssl", "enc", "-d", "-aes-256-cbc",
        "-K", key,
        "-iv", iv,
        "-in", enc_path
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        decrypted_content = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Phase 2 Failed: Decryption of {enc_path} failed. Ensure AES-256-CBC was used with the correct Key and IV. OpenSSL error: {e.stderr}")

    assert decrypted_content == "COMPLIANCE_AUDIT_PASSED_XYZ123", "Phase 2 Failed: Decrypted content does not match the expected audit flag."

def test_sandbox_blocks_socket():
    """
    Validates Phase 3 by running the sandbox with the 'test_net' argument
    to ensure the seccomp filter correctly blocks the socket system call.
    """
    sandbox_path = "/home/user/sandbox"
    assert os.path.exists(sandbox_path), "Phase 3 Failed: /home/user/sandbox executable does not exist."
    assert os.access(sandbox_path, os.X_OK), "Phase 3 Failed: /home/user/sandbox is not executable."

    cmd = [sandbox_path, "test_net"]

    # The sandbox should either kill the process (non-zero exit) or return an error (EPERM)
    # If it fails to block, legacy_auditd will print "Socket allowed!"
    result = subprocess.run(cmd, capture_output=True, text=True)

    stdout = result.stdout
    assert "Socket allowed!" not in stdout, "Phase 3 Failed: The sandbox did not block the socket system call. 'Socket allowed!' was printed."

    # Valid successful blocks will either crash (seccomp kill) or print "Socket blocked!"
    blocked_successfully = (result.returncode != 0) or ("Socket blocked!" in stdout)
    assert blocked_successfully, "Phase 3 Failed: The sandbox did not effectively block the socket call or handle it correctly."