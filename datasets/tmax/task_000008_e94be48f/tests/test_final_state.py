# test_final_state.py

import os
import struct
import pytest

def test_required_files_exist():
    """Verify that the user created the required scripts and output files."""
    assert os.path.isfile('/home/user/clean_join.c'), "/home/user/clean_join.c is missing."
    assert os.path.isfile('/home/user/process.sh'), "/home/user/process.sh is missing."
    assert os.path.isfile('/home/user/data/summary.txt'), "/home/user/data/summary.txt is missing."
    assert os.path.isfile('/home/user/data/cleaned.bin'), "/home/user/data/cleaned.bin is missing."

def test_summary_txt_content():
    """Verify that summary.txt contains the correct count of valid joined records."""
    with open('/home/user/data/summary.txt', 'r') as f:
        content = f.read().strip()
    assert content == "2", f"summary.txt should contain exactly '2', but found '{content}'."

def test_cleaned_bin_content():
    """Verify that cleaned.bin contains the correct binary data as per the struct definition."""
    with open('/home/user/data/cleaned.bin', 'rb') as f:
        data = f.read()

    assert len(data) == 48, f"cleaned.bin should be exactly 48 bytes (2 records * 24 bytes), but is {len(data)} bytes."

    # Struct format: 
    # Q: uint64_t (8 bytes)
    # I: uint32_t (4 bytes)
    # f: float (4 bytes)
    # 8s: char[8] (8 bytes)
    # Total: 24 bytes per record. Using little-endian '<' as standard for x86_64.

    records = []
    for i in range(2):
        chunk = data[i*24:(i+1)*24]
        ts, sid, adj, stat = struct.unpack('<QIf8s', chunk)
        # Decode status, ignoring errors and stripping null bytes
        stat_str = stat.decode('ascii', errors='ignore').rstrip('\x00')
        records.append((ts, sid, adj, stat_str))

    expected_record_1 = (1000, 1, 12.0, 'OK')
    expected_record_2 = (1001, 2, 4.0, 'WARN')

    assert records[0] == expected_record_1, f"Record 1 is incorrect. Expected {expected_record_1}, got {records[0]}"
    assert records[1] == expected_record_2, f"Record 2 is incorrect. Expected {expected_record_2}, got {records[1]}"