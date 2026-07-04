# test_final_state.py

import os
import pytest

def test_attacker_ips_file():
    """Test that attacker_ips.txt exists and contains the correct IP."""
    file_path = "/home/user/attacker_ips.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert set(lines) == {"10.0.0.5"}, f"Expected attacker IPs to be {{'10.0.0.5'}}, but got {set(lines)}"

def test_vulnerable_uris_file():
    """Test that vulnerable_uris.txt exists and contains the correct URIs."""
    file_path = "/home/user/vulnerable_uris.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_uris = {"/admin", "/profile"}
    assert set(lines) == expected_uris, f"Expected vulnerable URIs to be {expected_uris}, but got {set(lines)}"

def test_recovered_payloads_file():
    """Test that recovered_payloads.txt exists and contains the correct decrypted payloads."""
    file_path = "/home/user/recovered_payloads.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_payloads = {
        "EXFIL_START:flag{data_leak_1}",
        "EXFIL_START:flag{data_leak_2}"
    }
    assert set(lines) == expected_payloads, f"Expected recovered payloads to be {expected_payloads}, but got {set(lines)}"