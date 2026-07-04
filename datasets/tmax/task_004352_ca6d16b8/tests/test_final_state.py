# test_final_state.py

import os
import struct
import pytest

def parse_blob_file(filepath):
    """Yields (timestamp, chunk_data) for each chunk in the blob file."""
    with open(filepath, 'rb') as f:
        while True:
            header = f.read(32)
            if not header:
                break
            if len(header) < 32:
                pytest.fail(f"File {filepath} has an incomplete header.")

            magic, timestamp, payload_size, filename = struct.unpack("<4s Q I 16s", header)
            if magic != b"BLOB":
                pytest.fail(f"File {filepath} has invalid magic bytes: {magic}")

            payload = f.read(payload_size)
            if len(payload) < payload_size:
                pytest.fail(f"File {filepath} has an incomplete payload.")

            yield timestamp, header + payload

def get_expected_files_and_sizes():
    storage_pool = "/home/user/storage_pool"
    target_files = []
    total_original_bytes = 0
    total_compacted_bytes = 0
    expected_compacted_contents = {}

    for root, _, files in os.walk(storage_pool):
        for file in files:
            if file.endswith(".blob"):
                filepath = os.path.join(root, file)
                size = os.path.getsize(filepath)
                if size > 1048576:
                    target_files.append(file)
                    total_original_bytes += size

                    compacted_content = bytearray()
                    for timestamp, chunk_data in parse_blob_file(filepath):
                        if timestamp > 1700000000:
                            compacted_content.extend(chunk_data)

                    expected_compacted_contents[file] = bytes(compacted_content)
                    total_compacted_bytes += len(compacted_content)

    return expected_compacted_contents, total_original_bytes, total_compacted_bytes

def test_compacted_pool_directory_exists():
    assert os.path.isdir("/home/user/compacted_pool"), "/home/user/compacted_pool directory is missing."

def test_compacted_files_correctness():
    expected_contents, _, _ = get_expected_files_and_sizes()
    compacted_pool = "/home/user/compacted_pool"

    assert os.path.isdir(compacted_pool), "Compacted pool directory missing."

    actual_files = set(os.listdir(compacted_pool))
    expected_files = set(expected_contents.keys())

    assert actual_files == expected_files, f"Expected files {expected_files} in compacted_pool, but found {actual_files}."

    for filename, expected_data in expected_contents.items():
        filepath = os.path.join(compacted_pool, filename)
        with open(filepath, 'rb') as f:
            actual_data = f.read()
        assert actual_data == expected_data, f"The compacted file {filename} does not contain the exact expected valid chunks."

def test_reclaimed_space_report():
    report_path = "/home/user/reclaimed_space.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    _, expected_original, expected_compacted = get_expected_files_and_sizes()

    with open(report_path, 'r') as f:
        content = f.read().strip()

    expected_content = f"{expected_original} {expected_compacted}"
    assert content == expected_content, f"Expected report content '{expected_content}', but found '{content}'."