# test_final_state.py

import os
import json
import hashlib
import pytest

def get_expected_json(csv_path: str) -> str:
    """Reads the original UTF-16LE CSV and computes the expected minified JSON string."""
    with open(csv_path, 'rb') as f:
        content = f.read().decode('utf-16le')

    lines = [line.strip() for line in content.splitlines() if line.strip()]
    if not lines:
        return "[]"

    data = []
    for line in lines[1:]:
        parts = line.split(',', 2)
        if len(parts) == 3:
            data.append({
                "t": int(parts[0]),
                "s": parts[1],
                "m": parts[2]
            })

    # Minified JSON without spaces
    return json.dumps(data, separators=(',', ':'))

def test_rle_files_exist_and_correct():
    """Test that the RLE compressed files exist, follow strict RLE rules, and decompress to the correct JSON."""
    for log_name in ["log1", "log2"]:
        rle_path = f"/home/user/archive/{log_name}.json.rle"
        assert os.path.isfile(rle_path), f"Expected compressed file {rle_path} is missing."

        with open(rle_path, 'rb') as f:
            rle_data = f.read()

        assert len(rle_data) > 0, f"{rle_path} is empty."
        assert len(rle_data) % 2 == 0, f"{rle_path} length is not even; invalid strict RLE format."

        decompressed = bytearray()
        for i in range(0, len(rle_data), 2):
            count = rle_data[i]
            char = rle_data[i+1]

            assert 1 <= count <= 255, f"Invalid RLE count {count} at byte {i} in {rle_path}."
            decompressed.extend(bytes([char]) * count)

        csv_path = f"/home/user/legacy_logs/{log_name}.csv"
        expected_json = get_expected_json(csv_path)

        try:
            decompressed_str = decompressed.decode('utf-8')
        except UnicodeDecodeError:
            pytest.fail(f"Decompressed data from {rle_path} is not valid UTF-8.")

        assert decompressed_str == expected_json, f"Decompressed content of {rle_path} does not match the expected JSON."

def test_checksums_file():
    """Test that checksums.txt exists and contains the correct SHA-256 hashes for the decompressed JSON."""
    checksums_path = "/home/user/checksums.txt"
    assert os.path.isfile(checksums_path), f"{checksums_path} is missing."

    with open(checksums_path, 'r', encoding='utf-8') as f:
        content = f.read()

    for log_name in ["log1", "log2"]:
        csv_path = f"/home/user/legacy_logs/{log_name}.csv"
        expected_json = get_expected_json(csv_path)
        expected_hash = hashlib.sha256(expected_json.encode('utf-8')).hexdigest()

        expected_line = f"{expected_hash}  {log_name}.json"
        assert expected_line in content, f"Expected checksum line '{expected_line}' not found in {checksums_path}."