# test_final_state.py

import os
import struct
import pytest

WORKSPACE_DIR = "/home/user/workspace"
INDEX_BIN_PATH = os.path.join(WORKSPACE_DIR, "index.bin")
TEST_REPORT_PATH = os.path.join(WORKSPACE_DIR, "test_report.log")

def test_test_report_log():
    """Verify that test_report.log exists and contains exactly 'TEST_PASSED'."""
    assert os.path.exists(TEST_REPORT_PATH), f"{TEST_REPORT_PATH} does not exist."
    assert os.path.isfile(TEST_REPORT_PATH), f"{TEST_REPORT_PATH} is not a file."

    with open(TEST_REPORT_PATH, "r") as f:
        content = f.read().strip()

    assert content == "TEST_PASSED", f"Expected test_report.log to contain 'TEST_PASSED', but got: {content!r}"

def test_index_bin_structure_and_contents():
    """Verify that index.bin is generated correctly with the right sizes and checksums."""
    assert os.path.exists(INDEX_BIN_PATH), f"{INDEX_BIN_PATH} does not exist. Did the migrator run?"
    assert os.path.isfile(INDEX_BIN_PATH), f"{INDEX_BIN_PATH} is not a file."

    file_size = os.path.getsize(INDEX_BIN_PATH)
    expected_size = 8 + (3 * 70)
    assert file_size == expected_size, f"Expected {INDEX_BIN_PATH} to be {expected_size} bytes, but got {file_size} bytes."

    with open(INDEX_BIN_PATH, "rb") as f:
        data = f.read()

    # Check Header
    expected_header = b'\x49\x44\x58\x31\x02\x00\x03\x00'
    actual_header = data[0:8]
    assert actual_header == expected_header, f"Header mismatch. Expected {expected_header.hex()}, got {actual_header.hex()}"

    # Helper to parse an entry
    def parse_entry(offset):
        entry_data = data[offset:offset+70]
        filename = entry_data[0:64].rstrip(b'\x00').decode('ascii', errors='replace')
        size = struct.unpack('<I', entry_data[64:68])[0]
        checksum = struct.unpack('<H', entry_data[68:70])[0]
        return filename, size, checksum

    # Parse entries
    entries = []
    for i in range(3):
        offset = 8 + (i * 70)
        entries.append(parse_entry(offset))

    # We expect specific files in the registry. The order should match the CSV.
    expected_entries = [
        ("fileA.dat", 5, 0x094B),
        ("fileB.dat", 6, 0x2241),
        ("fileC.dat", 10, 0x5DFB)
    ]

    for i, (expected_name, expected_size, expected_checksum) in enumerate(expected_entries):
        actual_name, actual_size, actual_checksum = entries[i]
        assert actual_name == expected_name, f"Entry {i}: Expected filename {expected_name!r}, got {actual_name!r}"
        assert actual_size == expected_size, f"Entry {i} ({expected_name}): Expected size {expected_size}, got {actual_size}"
        assert actual_checksum == expected_checksum, f"Entry {i} ({expected_name}): Expected checksum 0x{expected_checksum:04X}, got 0x{actual_checksum:04X}"