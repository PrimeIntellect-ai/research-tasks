# test_final_state.py
import os
import pytest

def test_files_exist():
    expected_files = [
        '/home/user/rle_compress.py',
        '/home/user/archive.rle',
        '/home/user/verify.py',
        '/home/user/decompressed.txt'
    ]
    for filepath in expected_files:
        assert os.path.exists(filepath), f"File {filepath} is missing."

def test_compressor_uses_flock():
    compressor_path = '/home/user/rle_compress.py'
    assert os.path.isfile(compressor_path), f"{compressor_path} does not exist."

    with open(compressor_path, 'r') as f:
        code = f.read()

    assert 'fcntl' in code, "The compressor script must import and use fcntl."
    assert 'flock' in code, "The compressor script must use fcntl.flock."

def test_decompressed_content():
    decompressed_path = '/home/user/decompressed.txt'
    assert os.path.isfile(decompressed_path), f"{decompressed_path} does not exist."

    expected_lines = [
        "[INFO] Application started\n",
        "[INFO] Application started\n",
        "[WARN] High memory usage\n",
        "[WARN] High memory usage\n",
        "[WARN] High memory usage\n",
        "[INFO] User login\n",
        "[INFO] User login\n",
        "[ERROR] Connection timeout\n",
        "[ERROR] Connection timeout\n",
        "[INFO] Job finished\n",
        "[INFO] Job finished\n",
        "[INFO] Job finished\n"
    ]

    with open(decompressed_path, 'r') as f:
        actual_lines = f.readlines()

    assert sorted(actual_lines) == sorted(expected_lines), (
        "The decompressed output does not match the expected filtered logs. "
        "Ensure [DEBUG] lines are removed and counts are correct."
    )

def test_archive_rle_format():
    archive_path = '/home/user/archive.rle'
    assert os.path.isfile(archive_path), f"{archive_path} does not exist."

    with open(archive_path, 'r') as f:
        lines = f.readlines()

    assert len(lines) > 0, "The archive.rle file is empty."

    for line in lines:
        parts = line.split('|', 1)
        assert len(parts) == 2, f"Invalid RLE format in archive.rle: {line.strip()}"
        count_str, content = parts
        assert count_str.isdigit(), f"RLE count is not a number: {count_str}"
        assert int(count_str) > 0, f"RLE count must be positive: {count_str}"
        assert "[DEBUG]" not in content, f"DEBUG lines should have been filtered out: {content.strip()}"