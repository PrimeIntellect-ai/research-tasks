# test_final_state.py

import os
import pytest

def test_shared_library_exists():
    so_path = "/home/user/artifact_encoder/libencoder.so"
    assert os.path.isfile(so_path), f"Shared library {so_path} was not built or does not exist."

def test_encoded_artifacts():
    raw_dir = "/home/user/pipeline/raw_artifacts"
    enc_dir = "/home/user/pipeline/encoded_artifacts"

    assert os.path.isdir(raw_dir), f"Directory {raw_dir} is missing."
    assert os.path.isdir(enc_dir), f"Directory {enc_dir} is missing."

    raw_files = os.listdir(raw_dir)
    assert len(raw_files) > 0, "No raw artifacts found to verify."

    for raw_file in raw_files:
        raw_path = os.path.join(raw_dir, raw_file)
        enc_path = os.path.join(enc_dir, raw_file + ".enc")

        assert os.path.isfile(enc_path), f"Encoded artifact {enc_path} is missing."

        with open(raw_path, 'rb') as f:
            raw_data = f.read()

        with open(enc_path, 'rb') as f:
            enc_data = f.read()

        expected_data = bytes([b ^ 0x42 for b in raw_data])

        assert enc_data == expected_data, f"Encoded data in {enc_path} does not match expected XORed output."

def test_status_log():
    raw_dir = "/home/user/pipeline/raw_artifacts"
    log_path = "/home/user/pipeline/status.log"

    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    total_bytes = 0
    if os.path.isdir(raw_dir):
        for raw_file in os.listdir(raw_dir):
            raw_path = os.path.join(raw_dir, raw_file)
            if os.path.isfile(raw_path):
                total_bytes += os.path.getsize(raw_path)

    expected_log = f"Total bytes processed: {total_bytes}"

    with open(log_path, 'r') as f:
        actual_log = f.read().strip()

    assert actual_log == expected_log, f"Log file content is incorrect. Expected '{expected_log}', got '{actual_log}'."