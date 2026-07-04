# test_final_state.py

import os
import re
import hashlib
import pytest

def get_derived_truth():
    """
    Recomputes the expected final state by parsing the logs, decoding the payloads,
    hashing them, and matching against the malicious hashes file.
    """
    log_path = "/home/user/pentest_data/access.log"
    hashes_path = "/home/user/pentest_data/malicious_hashes.txt"

    assert os.path.exists(log_path), f"Missing log file: {log_path}"
    assert os.path.exists(hashes_path), f"Missing hashes file: {hashes_path}"

    with open(hashes_path, "r") as f:
        known_hashes = {line.strip() for line in f if line.strip()}

    matching_ip = None
    matching_payload = None

    with open(log_path, "r") as f:
        for line in f:
            # Extract IP and payload using regex
            match = re.search(r'^(\S+).*/api/auth\?payload=([0-9a-fA-F]+)', line)
            if match:
                ip = match.group(1)
                hex_payload = match.group(2)

                # Decode: Hex -> Bytes -> XOR 0x7F
                raw_bytes = bytes.fromhex(hex_payload)
                decoded_str = "".join(chr(b ^ 0x7F) for b in raw_bytes)

                # Hash the decoded string
                payload_hash = hashlib.sha256(decoded_str.encode('utf-8')).hexdigest()

                if payload_hash in known_hashes:
                    matching_ip = ip
                    matching_payload = decoded_str
                    break

    assert matching_ip is not None and matching_payload is not None, "Could not derive truth from provided data files."
    return matching_ip, matching_payload

def test_decoder_cpp_fixed():
    """
    Validates that the C++ decoder source code was modified to fix the logical bug.
    """
    cpp_path = "/home/user/pentest_data/decoder.cpp"
    assert os.path.exists(cpp_path), f"Missing decoder source file: {cpp_path}"

    with open(cpp_path, "r") as f:
        content = f.read()

    # The original bug was `i < hex_str.length() / 4`. 
    # A correct implementation would typically use `hex_str.length() / 2` or similar.
    assert "length() / 4" not in content.replace(" ", ""), "The C++ decoder still contains the 'length() / 4' bug."

def test_decoder_compiled():
    """
    Validates that the decoder was compiled to the expected path.
    """
    bin_path = "/home/user/pentest_data/decoder"
    assert os.path.exists(bin_path), f"Compiled decoder binary not found at {bin_path}"
    assert os.access(bin_path, os.X_OK), f"File at {bin_path} is not executable."

def test_report_content_matches_truth():
    """
    Validates that the final report exists and contains the correct IP and decoded payload.
    """
    report_path = "/home/user/report.txt"
    assert os.path.exists(report_path), f"Final report not found at {report_path}"

    expected_ip, expected_payload = get_derived_truth()

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Report should contain exactly two non-empty lines, found {len(lines)}."

    ip_line = lines[0]
    payload_line = lines[1]

    assert ip_line.startswith("IP: "), "First line of report must start with 'IP: '"
    assert payload_line.startswith("Payload: "), "Second line of report must start with 'Payload: '"

    actual_ip = ip_line.split("IP: ")[1].strip()
    actual_payload = payload_line.split("Payload: ")[1].strip()

    assert actual_ip == expected_ip, f"Reported IP '{actual_ip}' does not match the expected IP '{expected_ip}'."
    assert actual_payload == expected_payload, f"Reported Payload '{actual_payload}' does not match the expected Payload '{expected_payload}'."