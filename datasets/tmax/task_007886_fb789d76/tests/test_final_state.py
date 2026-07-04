# test_final_state.py

import os
import struct
import pytest

MANIFEST_PATH = "/home/user/backup_manifest.txt"
WAL_DATA_DIR = "/home/user/wal_data"

def compute_expected_manifest(wal_dir):
    valid_files = []

    if not os.path.isdir(wal_dir):
        return ""

    for filename in os.listdir(wal_dir):
        if not filename.endswith('.wal'):
            continue

        filepath = os.path.join(wal_dir, filename)
        if not os.path.isfile(filepath):
            continue

        file_size = os.path.getsize(filepath)
        if file_size < 16:
            continue

        with open(filepath, 'rb') as f:
            header = f.read(16)

        if len(header) < 16:
            continue

        magic = header[0:4]
        if magic != b'WAL!':
            continue

        seq = struct.unpack('<I', header[4:8])[0]
        payload_size = struct.unpack('<Q', header[8:16])[0]

        if file_size == 16 + payload_size:
            valid_files.append((seq, filename, payload_size))

    valid_files.sort(key=lambda x: x[0])

    lines = []
    for seq, filename, payload_size in valid_files:
        lines.append(f"{seq:08d} {filename} {payload_size}")

    return "\n".join(lines) + ("\n" if lines else "")

def test_manifest_exists():
    assert os.path.exists(MANIFEST_PATH), f"Manifest file {MANIFEST_PATH} was not created."
    assert os.path.isfile(MANIFEST_PATH), f"{MANIFEST_PATH} is not a regular file."

def test_manifest_contents():
    expected_content = compute_expected_manifest(WAL_DATA_DIR)

    with open(MANIFEST_PATH, 'r') as f:
        actual_content = f.read()

    # Normalize line endings and trailing whitespace for comparison
    expected_lines = [line.strip() for line in expected_content.strip().split('\n') if line.strip()]
    actual_lines = [line.strip() for line in actual_content.strip().split('\n') if line.strip()]

    assert actual_lines == expected_lines, (
        f"Manifest contents do not match expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )