# test_final_state.py

import os
import csv
import json
import hashlib
import pytest

def test_reclaimed_bytes():
    filepath = '/home/user/reclaimed_bytes.txt'
    assert os.path.exists(filepath), f"File {filepath} is missing"

    try:
        with open(filepath, 'r') as f:
            val_str = f.read().strip()
            val = int(val_str)
    except Exception as e:
        pytest.fail(f"Could not read an integer from {filepath}: {e}")

    expected_bytes = 12450000
    error = abs(val - expected_bytes)
    assert error <= 0, f"Metric error: {error}. Expected exactly {expected_bytes}, but got {val}."

def test_active_manifest():
    filepath = '/home/user/active_manifest.csv'
    assert os.path.exists(filepath), f"File {filepath} is missing"

    expected_entries = {
        ('F001', 'data_01.bin', 'ALPHA-10', '5000000'),
        ('F003', 'data_03.bin', 'BETA-22', '1500000'),
        ('F005', 'data_05.bin', 'GAMMA-05', '2000000'),
        ('F006', 'data_06.bin', 'ALPHA-10', '3500000'),
        ('F008', 'data_08.bin', 'BETA-22', '8000000')
    }

    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail(f"{filepath} is empty")

        assert header == ['file_id', 'filename', 'project_code', 'size_bytes'], \
            f"Invalid header in {filepath}. Got: {header}"

        actual_entries = set()
        for row in reader:
            if not row:
                continue
            assert len(row) == 4, f"Invalid row length in {filepath}: {row}"
            actual_entries.add(tuple(row))

    assert actual_entries == expected_entries, \
        f"Manifest entries do not match expected. Missing: {expected_entries - actual_entries}, Unexpected: {actual_entries - expected_entries}"

def test_modified_files_checksums():
    filepath = '/home/user/modified_files_checksums.txt'
    assert os.path.exists(filepath), f"File {filepath} is missing"

    expected_files = [
        '/home/user/storage_meta/batch1.csv',
        '/home/user/storage_meta/batch2.json',
        '/home/user/storage_meta/batch3.csv'
    ]

    expected_checksums = {}
    for ef in expected_files:
        assert os.path.exists(ef), f"Original file {ef} is missing, cannot compute checksum"
        with open(ef, 'rb') as f:
            expected_checksums[os.path.basename(ef)] = hashlib.sha256(f.read()).hexdigest()

    parsed_checksums = {}
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            assert len(parts) >= 2, f"Invalid checksum line format: {line}"
            checksum = parts[0]
            filename = os.path.basename(parts[1])
            parsed_checksums[filename] = checksum

    assert len(parsed_checksums) == len(expected_files), \
        f"Expected {len(expected_files)} files in checksum manifest, got {len(parsed_checksums)}"

    for filename, expected_hash in expected_checksums.items():
        assert filename in parsed_checksums, f"Missing checksum for {filename} in {filepath}"
        assert parsed_checksums[filename] == expected_hash, \
            f"Checksum mismatch for {filename}. Expected {expected_hash}, got {parsed_checksums[filename]}"