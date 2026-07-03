# test_final_state.py

import os
import pytest

def test_sanitized_payload_metric():
    """
    Validates that the sanitized payload exists, is a valid ELF file,
    has non-target IPs intact, and has target IPs correctly redacted.
    Calculates the Redaction Accuracy Score and asserts it is >= 1.0.
    """
    target_file = "/home/user/sanitized_payload.elf"

    assert os.path.exists(target_file), f"Expected output file {target_file} does not exist."

    with open(target_file, "rb") as f:
        data = f.read()

    # Check if it's still a valid ELF
    assert data.startswith(b"\x7fELF"), "The file is no longer a valid ELF binary. The ELF header is missing or corrupted."

    # Check if non-target IPs are intact
    assert b"192.168.1.100" in data, "Non-target IP '192.168.1.100' was modified or removed. It should remain intact."
    assert b"8.8.8.8" in data, "Non-target IP '8.8.8.8' was modified or removed. It should remain intact."

    # Check redaction of target IPs
    # Original lengths: "10.42.15.99" -> 11 chars -> "***********"
    # Original lengths: "10.42.200.1" -> 11 chars -> "***********"

    redacted_count = data.count(b"***********")

    target_ips_absent = (b"10.42.15.99" not in data) and (b"10.42.200.1" not in data)
    asterisks_present = redacted_count >= 2

    score = 1.0 if (target_ips_absent and asterisks_present) else 0.0

    assert score >= 1.0, f"Redaction Accuracy Score is {score}, expected >= 1.0. Target IPs were either not fully redacted or not replaced with the correct number of asterisks."