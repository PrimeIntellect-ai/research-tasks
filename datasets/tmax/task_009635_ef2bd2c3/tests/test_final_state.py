# test_final_state.py

import os
import pytest

EXPORT_DIR = "/home/user/export"
MANIFEST_FILE = "/home/user/manifest.csv"

def test_export_directory_exists():
    assert os.path.exists(EXPORT_DIR), f"Directory {EXPORT_DIR} does not exist."
    assert os.path.isdir(EXPORT_DIR), f"{EXPORT_DIR} is not a directory."

def test_exported_files():
    expected_files = {"alpha.hex", "gamma.hex", "omega.hex"}

    if not os.path.exists(EXPORT_DIR):
        pytest.fail(f"Export directory {EXPORT_DIR} is missing.")

    actual_files = set(os.listdir(EXPORT_DIR))

    missing = expected_files - actual_files
    extra = actual_files - expected_files

    assert not missing, f"Missing expected exported files: {missing}"
    assert not extra, f"Found unexpected files in export directory: {extra}"

@pytest.mark.parametrize("filename, expected_hex", [
    ("alpha.hex", "54657374446174614F6E65"),
    ("gamma.hex", "457861637454696D65"),
    ("omega.hex", "4C61737456616C696444617461"),
])
def test_exported_file_contents(filename, expected_hex):
    file_path = os.path.join(EXPORT_DIR, filename)
    assert os.path.exists(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == expected_hex, f"Content of {filename} is incorrect. Expected {expected_hex}, got {content}"

def test_manifest_file():
    assert os.path.exists(MANIFEST_FILE), f"Manifest file {MANIFEST_FILE} does not exist."
    assert os.path.isfile(MANIFEST_FILE), f"{MANIFEST_FILE} is not a file."

    expected_lines = [
        "alpha.bin,1700000005,11",
        "gamma.bin,1700000000,9",
        "omega.bin,1725000000,13"
    ]

    with open(MANIFEST_FILE, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert lines == expected_lines, f"Manifest contents are incorrect or incorrectly sorted. Expected {expected_lines}, got {lines}"