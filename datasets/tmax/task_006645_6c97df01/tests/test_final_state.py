# test_final_state.py

import os
import gzip
import hashlib
import pytest

def test_compress_logs_c_exists():
    path = "/home/user/compress_logs.c"
    assert os.path.isfile(path), f"Source file {path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert "#include" in content, f"{path} does not appear to be a valid C source file."

def test_archive_rle_gz_exists_and_valid():
    path = "/home/user/archive.rle.gz"
    assert os.path.isfile(path), f"Archive {path} is missing."

    expected_stream = "/home/user/active_logs/a.log\n4a4b2c\n/home/user/active_logs/b/c.log\n9x2x\n2y\n"

    try:
        with gzip.open(path, "rt", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        pytest.fail(f"Failed to read {path} as a gzip file: {e}")

    assert content == expected_stream, f"Decompressed content of {path} does not match the expected RLE output."

def test_archive_checksum_txt():
    path = "/home/user/archive_checksum.txt"
    assert os.path.isfile(path), f"Checksum file {path} is missing."

    with open(path, "r") as f:
        content = f.read().strip()

    # We can also compute the MD5 dynamically based on the expected stream
    expected_stream = "/home/user/active_logs/a.log\n4a4b2c\n/home/user/active_logs/b/c.log\n9x2x\n2y\n"
    expected_md5 = hashlib.md5(expected_stream.encode("utf-8")).hexdigest()

    # The task says the file should contain "just the hash string"
    assert content.startswith(expected_md5), f"Checksum in {path} is incorrect. Expected {expected_md5}, got {content}"