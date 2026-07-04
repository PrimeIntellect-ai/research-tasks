# test_final_state.py

import os
import subprocess
import struct
import pytest

def fnv1a_64(text):
    hash_val = 14695981039346656037
    for char in text:
        hash_val = hash_val ^ ord(char)
        hash_val = (hash_val * 1099511628211) & 0xffffffffffffffff
    return hash_val

def test_pipeline_and_output():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Pipeline script failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

    bin_path = "/home/user/store.bin"
    assert os.path.isfile(bin_path), f"Output file {bin_path} does not exist."

    csv_path = "/home/user/data.csv"
    assert os.path.isfile(csv_path), f"Input file {csv_path} does not exist."

    expected_records = []
    with open(csv_path, "r") as f:
        lines = f.read().strip().split('\n')
        if lines:
            lines = lines[1:] # Skip header
        for line in lines:
            if not line.strip():
                continue
            parts = line.split(',', 2)
            if len(parts) != 3:
                continue
            id_str, cat, text = parts
            try:
                record_id = int(id_str)
            except ValueError:
                continue

            if record_id <= 0:
                continue
            if cat not in ("A", "B", "C"):
                continue
            if not text:
                continue

            cat_bytes = cat.encode('ascii').ljust(4, b'\x00')
            fingerprint = fnv1a_64(text)
            expected_records.append((record_id, cat_bytes, fingerprint))

    record_size = struct.calcsize('<i4sQ')

    with open(bin_path, "rb") as f:
        data = f.read()

    expected_size = len(expected_records) * record_size
    assert len(data) == expected_size, f"File size mismatch: expected {expected_size} bytes, got {len(data)} bytes."

    for i, expected in enumerate(expected_records):
        chunk = data[i*record_size : (i+1)*record_size]
        actual = struct.unpack('<i4sQ', chunk)
        assert actual == expected, f"Mismatch at record index {i}:\nExpected: {expected}\nGot: {actual}"