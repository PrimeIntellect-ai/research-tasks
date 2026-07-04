# test_final_state.py

import os
import pytest

REPORT_PATH = "/home/user/investigation_report.txt"
TARGET_FILE_PATH = "/home/user/.conf_7781a"
PCAP_PORT = "8443"

def compute_expected_hex(data: str) -> str:
    """Derives the expected hex output based on the malware's encoding logic."""
    fib = [1, 1]
    for i in range(2, 10):
        fib.append(fib[i-1] + fib[i-2])

    encoded_chars = []
    for i, char in enumerate(data):
        # The C code uses: unsigned char encoded = data[i] + fib[i % 10]
        encoded_val = (ord(char) + fib[i % 10]) & 0xFF
        encoded_chars.append(f"{encoded_val:02x}")

    return "".join(encoded_chars)

def test_investigation_report_exists():
    assert os.path.isfile(REPORT_PATH), f"The investigation report file is missing at {REPORT_PATH}."

def test_investigation_report_contents():
    with open(REPORT_PATH, "r") as f:
        lines = [line.strip() for line in f.read().strip().split('\n')]

    assert len(lines) == 3, f"Expected exactly 3 lines in {REPORT_PATH}, but found {len(lines)}."

    # Line 1: Target file path
    assert lines[0] == TARGET_FILE_PATH, f"Line 1 of the report is incorrect. Expected the absolute path of the hidden file, got: '{lines[0]}'"

    # Line 2: Destination port
    assert lines[1] == PCAP_PORT, f"Line 2 of the report is incorrect. Expected the destination TCP port, got: '{lines[1]}'"

    # Line 3: Hex output
    # Read the actual content of the target file to compute the expected hex
    assert os.path.isfile(TARGET_FILE_PATH), f"Target file {TARGET_FILE_PATH} is missing, cannot verify hex output."
    with open(TARGET_FILE_PATH, "r") as f:
        target_data = f.read()

    expected_hex = compute_expected_hex(target_data)
    assert lines[2] == expected_hex, f"Line 3 of the report is incorrect. Expected the hex output of the repaired malware, got: '{lines[2]}'"

def test_malware_c_fixed():
    c_file = "/home/user/malware.c"
    assert os.path.isfile(c_file), f"The source file {c_file} is missing."

    with open(c_file, "r") as f:
        content = f.read()

    assert "i <= 10" not in content, f"The off-by-one error (i <= 10) is still present in {c_file}."
    assert "i < 10" in content, f"The loop boundary in {c_file} was not fixed to 'i < 10' as expected."