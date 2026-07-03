# test_final_state.py

import os
import struct
import pytest

def test_archive_bin_exists():
    assert os.path.isfile("/home/user/archive.bin"), "The output file /home/user/archive.bin was not created."

def test_archive_bin_content():
    try:
        with open("/home/user/archive.bin", "rb") as f:
            data = f.read()
    except Exception as e:
        pytest.fail(f"Could not read /home/user/archive.bin: {e}")

    assert len(data) >= 4, "File is too short to contain the header."
    assert data[:4] == b'BKP1', f"Invalid header in archive.bin. Expected b'BKP1', got {data[:4]}"

    offset = 4
    records = []
    while offset < len(data):
        assert offset + 11 <= len(data), "Truncated record found in archive.bin (not enough bytes for header)."

        ts = struct.unpack("<Q", data[offset:offset+8])[0]
        sev = struct.unpack("<B", data[offset+8:offset+9])[0]
        length = struct.unpack("<H", data[offset+9:offset+11])[0]
        offset += 11

        assert offset + length <= len(data), f"Truncated record found in archive.bin (message length {length} exceeds remaining bytes)."

        try:
            msg = data[offset:offset+length].decode('utf-8')
        except UnicodeDecodeError:
            pytest.fail("Message bytes could not be decoded as UTF-8.")

        offset += length
        records.append((ts, sev, msg))

    expected = [
        (1700000000, 0, "Service started successfully."),
        (1700000005, 1, "High memory usage\ndetected on node A."),
        (1700000010, 2, "Database connection lost!\nRetrying...\nFailed.")
    ]

    assert len(records) == len(expected), f"Expected {len(expected)} records, but found {len(records)} in archive.bin."

    for i, (actual, exp) in enumerate(zip(records, expected)):
        assert actual[0] == exp[0], f"Record {i+1}: Expected timestamp {exp[0]}, got {actual[0]}."
        assert actual[1] == exp[1], f"Record {i+1}: Expected severity {exp[1]}, got {actual[1]}."
        assert actual[2] == exp[2], f"Record {i+1}: Expected message {repr(exp[2])}, got {repr(actual[2])}."