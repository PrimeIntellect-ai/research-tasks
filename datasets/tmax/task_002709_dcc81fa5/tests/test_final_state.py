# test_final_state.py

import os
import hashlib
import pytest

LOG_FILE = "/home/user/sec_events.log"
CERTS_FILE = "/home/user/revoked_certs.txt"
BIN_FILE = "/home/user/known_good.bin"
OUTPUT_FILE = "/home/user/compromised_ips.txt"

def get_expected_compromised_ips():
    """Dynamically calculates the expected compromised IPs based on the setup files."""
    # Read revoked certificates
    with open(CERTS_FILE, 'r') as f:
        revoked_certs = set(line.strip() for line in f if line.strip())

    # Calculate SHA-256 hash of the known good binary
    with open(BIN_FILE, 'rb') as f:
        known_good_hash = hashlib.sha256(f.read()).hexdigest()

    expected_ips = set()

    # Parse the security events log
    with open(LOG_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split('|')
            if len(parts) != 4:
                continue

            ip, cert, csp, file_hash = parts

            # Evaluate criteria
            is_revoked_cert = cert in revoked_certs
            is_weak_csp = "default-src 'self'" not in csp
            is_bad_hash = file_hash != known_good_hash

            # Endpoint is compromised only if ALL conditions are met
            if is_revoked_cert and is_weak_csp and is_bad_hash:
                expected_ips.add(ip)

    return expected_ips

def test_output_file_exists():
    """Test that the compromised_ips.txt file was created."""
    assert os.path.isfile(OUTPUT_FILE), f"The required output file {OUTPUT_FILE} was not created."

def test_compromised_ips_correct():
    """Test that the compromised_ips.txt file contains exactly the correct IPs."""
    assert os.path.isfile(OUTPUT_FILE), f"Cannot verify contents because {OUTPUT_FILE} is missing."

    expected_ips = get_expected_compromised_ips()

    with open(OUTPUT_FILE, 'r') as f:
        actual_ips = set(line.strip() for line in f if line.strip())

    missing_ips = expected_ips - actual_ips
    extra_ips = actual_ips - expected_ips

    error_messages = []
    if missing_ips:
        error_messages.append(f"Missing expected compromised IPs: {', '.join(missing_ips)}")
    if extra_ips:
        error_messages.append(f"Found unexpected IPs that should not be marked compromised: {', '.join(extra_ips)}")

    assert not missing_ips and not extra_ips, " | ".join(error_messages)