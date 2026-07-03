# test_final_state.py
import os
import subprocess
import time
import pytest
import re

def test_cwes_identified():
    """Test that the correct CWEs are identified in cwes.txt."""
    cwes_file = "/home/user/cwes.txt"
    assert os.path.isfile(cwes_file), f"Missing file: {cwes_file}"

    with open(cwes_file, "r") as f:
        content = f.read().upper()

    # Check for hardcoded credentials
    assert "CWE-798" in content, "cwes.txt is missing CWE-798 (hardcoded credentials)"

    # Check for auth bypass
    bypass_cwes = ["CWE-288", "CWE-287", "CWE-807"]
    assert any(cwe in content for cwe in bypass_cwes), f"cwes.txt is missing an auth bypass CWE (expected one of {bypass_cwes})"

    # Check for cleartext sensitive info
    sensitive_cwes = ["CWE-532", "CWE-312"]
    assert any(cwe in content for cwe in sensitive_cwes), f"cwes.txt is missing a sensitive info CWE (expected one of {sensitive_cwes})"

def test_exploit_script_execution():
    """Test that the exploit script successfully bypasses authentication and retrieves the token."""
    exploit_script = "/home/user/exploit.sh"
    server_script = "/home/user/server.py"

    assert os.path.isfile(exploit_script), f"Missing file: {exploit_script}"
    assert os.access(exploit_script, os.X_OK), f"{exploit_script} is not executable"

    # Start the server
    server_process = subprocess.Popen(["python3", server_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1) # Wait for server to start

    try:
        # Run the exploit script
        result = subprocess.run([exploit_script], capture_output=True, text=True, timeout=5)
        output = result.stdout.strip()

        assert "FLG_77b31_s3cr3t" in output, f"Exploit script did not output the correct secret token. Output was: {output}"
        # Ensure it ONLY outputs the token or at least contains it as the primary result
        assert output.endswith("FLG_77b31_s3cr3t") or "FLG_77b31_s3cr3t" in output.split(), "Exploit script should print the secret token."
    finally:
        server_process.terminate()
        server_process.wait()

def test_redact_script_and_clean_log():
    """Test that the redact script exists, is executable, and clean.log is properly redacted."""
    redact_script = "/home/user/redact.sh"
    clean_log = "/home/user/clean.log"

    assert os.path.isfile(redact_script), f"Missing file: {redact_script}"
    assert os.access(redact_script, os.X_OK), f"{redact_script} is not executable"
    assert os.path.isfile(clean_log), f"Missing file: {clean_log}"

    with open(clean_log, "r") as f:
        content = f.read()

    # Check that SSNs are redacted
    assert "123-45-6789" not in content, "clean.log still contains an unredacted SSN"
    assert "987-65-4321" not in content, "clean.log still contains an unredacted SSN"
    assert "[REDACTED_SSN]" in content, "clean.log is missing the [REDACTED_SSN] string"

    # Check that emails are redacted
    assert "alice.smith@example.com" not in content, "clean.log still contains an unredacted email"
    assert "bob_jones@domain.co.uk" not in content, "clean.log still contains an unredacted email"
    assert "charlie+test@sub.domain.org" not in content, "clean.log still contains an unredacted email"
    assert "[REDACTED_EMAIL]" in content, "clean.log is missing the [REDACTED_EMAIL] string"

    # Check for original structure
    assert "User registered: Alice Smith" in content, "clean.log is missing original non-sensitive log text"
    assert "Failed login attempt for" in content, "clean.log is missing original non-sensitive log text"
    assert "Payment processed for Charlie" in content, "clean.log is missing original non-sensitive log text"