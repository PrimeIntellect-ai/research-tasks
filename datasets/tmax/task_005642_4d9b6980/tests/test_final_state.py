# test_final_state.py
import os
import gzip
import struct
import pytest

def test_completion_file_exists():
    """Verify that the completion.txt file exists and contains 'DONE'."""
    completion_file = "/home/user/completion.txt"
    assert os.path.isfile(completion_file), f"Completion file {completion_file} is missing."
    with open(completion_file, "r") as f:
        content = f.read().strip()
    assert content == "DONE", f"Completion file content is '{content}', expected 'DONE'."

def test_files_renamed_and_compressed():
    """Verify that original CSVs are renamed to .bak and .bin.gz are created."""
    bases = ["app_a", "app_b", "app_c"]
    for base in bases:
        csv_path = f"/home/user/logs/{base}.csv"
        bak_path = f"/home/user/logs/{base}.csv.bak"
        bin_path = f"/home/user/logs/{base}.bin.gz"

        assert not os.path.exists(csv_path), f"Original file {csv_path} should have been renamed."
        assert os.path.isfile(bak_path), f"Backup file {bak_path} is missing."
        assert os.path.isfile(bin_path), f"Compressed binary file {bin_path} is missing."

def test_binary_data_correctness():
    """Verify that the .bin.gz files contain the correct packed binary data matching the .bak files."""
    bases = ["app_a", "app_b", "app_c"]
    record_struct = struct.Struct("<QIHI")
    record_size = record_struct.size  # Should be 18 bytes

    for base in bases:
        bak_path = f"/home/user/logs/{base}.csv.bak"
        bin_path = f"/home/user/logs/{base}.bin.gz"

        if not os.path.isfile(bak_path) or not os.path.isfile(bin_path):
            continue  # Handled by previous test

        with open(bak_path, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        try:
            with gzip.open(bin_path, "rb") as f:
                binary_data = f.read()
        except Exception as e:
            pytest.fail(f"Failed to decompress {bin_path}: {e}")

        assert len(binary_data) == len(lines) * record_size, \
            f"Size of decompressed data in {bin_path} does not match the expected size for {len(lines)} records."

        for i, line in enumerate(lines):
            parts = line.split(",")
            assert len(parts) == 4, f"Invalid CSV format in {bak_path} at line {i+1}"

            expected_timestamp = int(parts[0])
            expected_user_id = int(parts[1])
            expected_action_code = int(parts[2])
            expected_payload_size = int(parts[3])

            offset = i * record_size
            record_bytes = binary_data[offset:offset + record_size]

            try:
                timestamp, user_id, action_code, payload_size = record_struct.unpack(record_bytes)
            except struct.error as e:
                pytest.fail(f"Failed to unpack record {i+1} in {bin_path}: {e}")

            assert timestamp == expected_timestamp, f"Record {i+1} in {bin_path}: timestamp mismatch. Expected {expected_timestamp}, got {timestamp}."
            assert user_id == expected_user_id, f"Record {i+1} in {bin_path}: user_id mismatch. Expected {expected_user_id}, got {user_id}."
            assert action_code == expected_action_code, f"Record {i+1} in {bin_path}: action_code mismatch. Expected {expected_action_code}, got {action_code}."
            assert payload_size == expected_payload_size, f"Record {i+1} in {bin_path}: payload_size mismatch. Expected {expected_payload_size}, got {payload_size}."