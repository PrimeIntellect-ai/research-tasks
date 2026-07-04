# test_final_state.py

import os
import gzip
import hashlib
import pytest

def test_archiver_cpp_exists():
    assert os.path.isfile("/home/user/archiver.cpp"), "The C++ source file /home/user/archiver.cpp is missing."

def test_archiver_binary_exists():
    assert os.path.isfile("/home/user/archiver"), "The compiled binary /home/user/archiver is missing."
    assert os.access("/home/user/archiver", os.X_OK), "The file /home/user/archiver is not executable."

def test_curated_archive_content():
    archive_path = "/home/user/curated_archive.gz"
    assert os.path.isfile(archive_path), f"The archive {archive_path} is missing."

    expected_content = b"chunk_A_data_chunk_B_data_chunk_D_datachunk_C_data_"

    try:
        with gzip.open(archive_path, "rb") as f:
            actual_content = f.read()
    except Exception as e:
        pytest.fail(f"Failed to read {archive_path} as a gzip file: {e}")

    assert actual_content == expected_content, "The uncompressed content of the archive does not match the expected combined binary stream."

def test_checksum_txt_content():
    checksum_path = "/home/user/checksum.txt"
    assert os.path.isfile(checksum_path), f"The checksum file {checksum_path} is missing."

    expected_hash = "4e0f269a941da7e3f890c29b9ef96e1a4de110c497330a8459ce798939c1b721"

    with open(checksum_path, "r") as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"The checksum in {checksum_path} is incorrect. Expected {expected_hash}, got {actual_hash}."