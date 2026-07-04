# test_final_state.py

import os
import pytest

INCOMING_DIR = "/home/user/incoming_data"
ORGANIZED_DIR = "/home/user/organized_data"

def test_chunk_a_processed_correctly():
    expected_file = os.path.join(ORGANIZED_DIR, "class_1", "chunk_a.dat.rle")
    assert os.path.isfile(expected_file), f"Expected processed file {expected_file} is missing."

    with open(expected_file, "rb") as f:
        content = f.read()

    expected_content = bytes([0x41, 0x05, 0x42, 0x05])
    assert content == expected_content, f"Content of {expected_file} is incorrect. Expected {expected_content.hex()}, got {content.hex()}."

def test_chunk_d_processed_correctly():
    expected_file = os.path.join(ORGANIZED_DIR, "class_5", "chunk_d.dat.rle")
    assert os.path.isfile(expected_file), f"Expected processed file {expected_file} is missing."

    with open(expected_file, "rb") as f:
        content = f.read()

    expected_content = bytes([0x58, 0xFF, 0x58, 0x2D, 0x59, 0x02])
    assert content == expected_content, f"Content of {expected_file} is incorrect. Expected {expected_content.hex()}, got {content.hex()}."

def test_invalid_chunks_skipped():
    # chunk_b has no ready file, chunk_c has invalid magic. Neither should be processed.
    for root, dirs, files in os.walk(ORGANIZED_DIR):
        for file in files:
            assert "chunk_b" not in file, f"Found {file} in {ORGANIZED_DIR}, but chunk_b should have been skipped (no .ready file)."
            assert "chunk_c" not in file, f"Found {file} in {ORGANIZED_DIR}, but chunk_c should have been skipped (invalid magic number)."

def test_original_files_not_deleted():
    original_files = [
        "chunk_a.dat", "chunk_a.ready",
        "chunk_b.dat",
        "chunk_c.dat", "chunk_c.ready",
        "chunk_d.dat", "chunk_d.ready"
    ]
    for filename in original_files:
        filepath = os.path.join(INCOMING_DIR, filename)
        assert os.path.isfile(filepath), f"Original file {filepath} was deleted, but instructions said 'Do not delete the original files'."