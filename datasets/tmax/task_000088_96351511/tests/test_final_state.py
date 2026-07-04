# test_final_state.py

import os
import hashlib
import struct
import pytest

DATASET_DIR = "/home/user/dataset"
FILES_TXT = os.path.join(DATASET_DIR, "files.txt")
PARSER_CPP = "/home/user/parser.cpp"
PARSER_BIN = "/home/user/parser"
MANIFEST_CSV = "/home/user/manifest.csv"

def get_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def test_files_txt_cleaned():
    assert os.path.isfile(FILES_TXT), f"{FILES_TXT} is missing."
    with open(FILES_TXT, "r") as f:
        content = f.read()

    # Ensure Windows paths are gone and Linux paths are present
    assert "C:\\dataset\\" not in content, "Windows paths were not removed from files.txt"
    assert "/home/user/dataset/alpha.dat" in content, "Cleaned path for alpha.dat not found in files.txt"
    assert "/home/user/dataset/beta.dat" in content, "Cleaned path for beta.dat not found in files.txt"
    assert "/home/user/dataset/gamma.dat" in content, "Cleaned path for gamma.dat not found in files.txt"

def test_parser_exists_and_compiled():
    assert os.path.isfile(PARSER_CPP), f"Source file {PARSER_CPP} is missing."
    assert os.path.isfile(PARSER_BIN), f"Compiled binary {PARSER_BIN} is missing."
    assert os.access(PARSER_BIN, os.X_OK), f"{PARSER_BIN} is not executable."

def test_parser_uses_locking():
    assert os.path.isfile(PARSER_CPP), f"Source file {PARSER_CPP} is missing."
    with open(PARSER_CPP, "r") as f:
        content = f.read()

    assert "flock" in content or "fcntl" in content, "C++ source does not appear to use explicit file locking (flock or fcntl)."

def test_manifest_csv_correctness():
    assert os.path.isfile(MANIFEST_CSV), f"{MANIFEST_CSV} was not generated."

    with open(MANIFEST_CSV, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Generate expected data
    expected_files = ["alpha.dat", "beta.dat", "gamma.dat"]
    expected_rows = []

    for filename in expected_files:
        filepath = os.path.join(DATASET_DIR, filename)
        assert os.path.isfile(filepath), f"Expected data file {filepath} is missing."

        with open(filepath, "rb") as f:
            header_data = f.read(16)
            _, sensor_id, timestamp = struct.unpack("<4s I Q", header_data)

        file_hash = get_sha256(filepath)
        expected_rows.append(f"{filename},{sensor_id},{timestamp},{file_hash}")

    assert len(lines) == 3, f"Expected exactly 3 rows in manifest.csv, found {len(lines)}."

    for expected_row in expected_rows:
        assert expected_row in lines, f"Expected row '{expected_row}' not found in manifest.csv."

    # Ensure corrupt.dat is not in the manifest
    for line in lines:
        assert "corrupt.dat" not in line, "corrupt.dat should have been skipped but was found in manifest.csv."