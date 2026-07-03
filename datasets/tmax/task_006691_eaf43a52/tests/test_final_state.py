# test_final_state.py

import os
import hashlib
import pytest

def test_chunks_directory_exists():
    """Test that the chunks directory exists."""
    chunks_dir = "/home/user/chunks"
    assert os.path.exists(chunks_dir), f"Directory {chunks_dir} does not exist."
    assert os.path.isdir(chunks_dir), f"{chunks_dir} is not a directory."

def test_chunk_files_content():
    """Test that the chunk files exist and contain the correct payloads."""
    expected_chunks = {
        "chunk_1680000000.dat": b'A' * 1024,
        "chunk_1680000060.dat": b'B' * 2048,
        "chunk_1680000120.dat": b'C' * 512,
        "chunk_1680000180.dat": b'D' * 4096,
    }

    chunks_dir = "/home/user/chunks"

    for filename, expected_content in expected_chunks.items():
        filepath = os.path.join(chunks_dir, filename)
        assert os.path.exists(filepath), f"Expected chunk file {filepath} is missing."
        assert os.path.isfile(filepath), f"{filepath} is not a file."

        with open(filepath, "rb") as f:
            content = f.read()

        assert len(content) == len(expected_content), f"File {filename} has incorrect size. Expected {len(expected_content)}, got {len(content)}."
        assert content == expected_content, f"File {filename} content does not match the expected payload."

def test_extraction_log():
    """Test that the extraction log contains the correct CSV data."""
    log_path = "/home/user/extraction_log.csv"
    assert os.path.exists(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read().strip().splitlines()

    # The task asks for 'Timestamp,PayloadSize' header, but allows some flexibility.
    # We will check that the expected data rows are present in order.
    expected_rows = [
        "1680000000,1024",
        "1680000060,2048",
        "1680000120,512",
        "1680000180,4096"
    ]

    # Filter out empty lines or the header if present
    data_rows = [line.strip() for line in content if line.strip() and line.strip() != "Timestamp,PayloadSize"]

    assert data_rows == expected_rows, f"Extraction log data does not match expected output. Got: {data_rows}"

def test_processor_c_exists_and_uses_mmap():
    """Test that the C program exists and uses mmap."""
    source_path = "/home/user/processor.c"
    assert os.path.exists(source_path), f"C source file {source_path} is missing."

    with open(source_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    assert "mmap" in content, f"The C source file {source_path} does not appear to use 'mmap'."