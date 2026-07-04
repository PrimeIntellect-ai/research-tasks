# test_final_state.py
import os
import hashlib
import pytest

def get_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def test_chunk_files_created():
    output_dir = "/home/user/archive_output"

    expected_files = {
        "experiments_run1_sensor_data.dat_part0.chunk": (1024, b"B" * 1024),
        "experiments_run1_sensor_data.dat_part1.chunk": (476, b"B" * 476),
        "main_data.dat_part0.chunk": (1024, b"A" * 1024),
        "main_data.dat_part1.chunk": (1024, b"A" * 1024),
        "main_data.dat_part2.chunk": (452, b"A" * 452),
    }

    for filename, (expected_size, expected_content) in expected_files.items():
        filepath = os.path.join(output_dir, filename)
        assert os.path.isfile(filepath), f"Expected chunk file is missing: {filepath}"

        with open(filepath, "rb") as f:
            content = f.read()

        assert len(content) == expected_size, f"Incorrect file size for {filename}. Expected {expected_size}, got {len(content)}."
        assert content == expected_content, f"Incorrect file content for {filename}."

def test_manifest_file():
    manifest_path = "/home/user/archive_output/manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file is missing: {manifest_path}"

    expected_lines = [
        f"{get_sha256(b'B'*1024)}  experiments_run1_sensor_data.dat_part0.chunk",
        f"{get_sha256(b'B'*476)}  experiments_run1_sensor_data.dat_part1.chunk",
        f"{get_sha256(b'A'*1024)}  main_data.dat_part0.chunk",
        f"{get_sha256(b'A'*1024)}  main_data.dat_part1.chunk",
        f"{get_sha256(b'A'*452)}  main_data.dat_part2.chunk"
    ]

    with open(manifest_path, "r", encoding="utf-8") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Manifest has incorrect number of lines. Expected {len(expected_lines)}, got {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Manifest line {i+1} is incorrect.\nExpected: '{expected}'\nGot:      '{actual}'"

def test_no_extra_chunks():
    output_dir = "/home/user/archive_output"
    allowed_files = {
        "experiments_run1_sensor_data.dat_part0.chunk",
        "experiments_run1_sensor_data.dat_part1.chunk",
        "main_data.dat_part0.chunk",
        "main_data.dat_part1.chunk",
        "main_data.dat_part2.chunk",
        "manifest.txt"
    }

    actual_files = set(os.listdir(output_dir))
    extra_files = actual_files - allowed_files

    assert not extra_files, f"Found unexpected files in output directory: {extra_files}. Cycle detection may have failed or ignored files were processed."