# test_final_state.py
import os
import re

def test_token_extracted():
    token_path = "/home/user/token.txt"
    assert os.path.isfile(token_path), f"{token_path} does not exist."

    with open(token_path, "r") as f:
        token = f.read().strip()

    expected_token = "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4"
    assert token == expected_token, f"Token in {token_path} is incorrect. Expected {expected_token}, got {token}."

def test_clean_log_exists():
    log_path = "/home/user/clean.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

def test_clean_log_redaction():
    log_path = "/home/user/clean.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read()

    # Check SSNs
    assert "***-**-****" in content, "SSNs were not redacted properly in clean.log."
    assert "123-45-6789" not in content, "Unredacted SSN (123-45-6789) found in clean.log."
    assert "555-12-3456" not in content, "Unredacted SSN (555-12-3456) found in clean.log."

    # Check CCs
    assert "************4444" in content, "CC ending in 4444 was not redacted properly in clean.log."
    assert "4111222233334444" not in content, "Unredacted CC (4111222233334444) found in clean.log."

    assert "************7654" in content, "CC ending in 7654 was not redacted properly in clean.log."
    assert "9876543210987654" not in content, "Unredacted CC (9876543210987654) found in clean.log."

def test_clean_log_long_line():
    log_path = "/home/user/clean.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read()

    long_line = "LONG: This is a very long line that would normally cause a buffer overflow because it exceeds the one hundred and twenty eight character limit that was hardcoded into the extremely poorly written legacy cpp application that we are testing right now."
    assert long_line in content, "The long line was truncated or is missing in clean.log, indicating the buffer overflow was not properly fixed."

def test_sshd_config():
    config_path = "/home/user/sshd_config"
    assert os.path.isfile(config_path), f"{config_path} does not exist."

    with open(config_path, "r") as f:
        content = f.read()

    # Normalize whitespace for checking directives, ignore comments
    lines = [line.strip() for line in content.splitlines() if line.strip() and not line.strip().startswith("#")]

    def check_directive(directive, expected_value):
        # Match directive and value separated by space or equals sign
        pattern = re.compile(rf"^{directive}[\s=]+{expected_value}$", re.IGNORECASE)
        for line in lines:
            if pattern.match(line):
                return True
        return False

    assert check_directive("Port", "2222"), "Port 2222 directive missing or incorrect in sshd_config."
    assert check_directive("PasswordAuthentication", "no"), "PasswordAuthentication no directive missing or incorrect in sshd_config."
    assert check_directive("X11Forwarding", "no"), "X11Forwarding no directive missing or incorrect in sshd_config."
    assert check_directive("PermitRootLogin", "no"), "PermitRootLogin no directive missing or incorrect in sshd_config."
    assert check_directive("AllowUsers", "user"), "AllowUsers user directive missing or incorrect in sshd_config."
    assert check_directive("MACs", "hmac-sha2-256"), "MACs hmac-sha2-256 directive missing or incorrect in sshd_config."