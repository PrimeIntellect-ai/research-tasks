# test_final_state.py

import os
import pytest

RAW_DATASET_DIR = "/home/user/raw_dataset"
CLEAN_DATASET_DIR = "/home/user/clean_dataset"
MANIFEST_FILE = "/home/user/backup_manifest.csv"

VALID_FILES = [
    ("scan_root.dat", 20, b"BRAN" + b"\x00" * 16),
    ("subject1/scan1.dat", 8, b"BRAN" + b"\x01\x02\x03\x04"),
    ("subject2/sessionA/scanA.dat", 14, b"BRAN" + b"\xFF" * 10),
    ("subject3/scan3.dat", 104, b"BRAN" + b"\x0A" * 100),
]

INVALID_FILES = [
    "subject1/corrupt.dat",
    "subject2/sessionB/short.dat",
]

def test_clean_dataset_exists():
    assert os.path.isdir(CLEAN_DATASET_DIR), f"Directory {CLEAN_DATASET_DIR} does not exist."

@pytest.mark.parametrize("rel_path, size, content", VALID_FILES)
def test_valid_files_copied(rel_path, size, content):
    dest_path = os.path.join(CLEAN_DATASET_DIR, rel_path)
    assert os.path.isfile(dest_path), f"Valid file {rel_path} was not copied to {CLEAN_DATASET_DIR}."
    assert os.path.getsize(dest_path) == size, f"File {rel_path} size mismatch. Expected {size}, got {os.path.getsize(dest_path)}."
    with open(dest_path, "rb") as f:
        assert f.read() == content, f"File {rel_path} content mismatch."

@pytest.mark.parametrize("rel_path", INVALID_FILES)
def test_invalid_files_not_copied(rel_path):
    dest_path = os.path.join(CLEAN_DATASET_DIR, rel_path)
    assert not os.path.exists(dest_path), f"Invalid file {rel_path} should not have been copied."

def test_manifest_file():
    assert os.path.isfile(MANIFEST_FILE), f"Manifest file {MANIFEST_FILE} does not exist."

    expected_lines = [
        "scan_root.dat,20",
        "subject1/scan1.dat,8",
        "subject2/sessionA/scanA.dat,14",
        "subject3/scan3.dat,104"
    ]

    with open(MANIFEST_FILE, "r") as f:
        content = f.read().strip()

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, f"Manifest file content mismatch. Expected:\n{expected_lines}\nGot:\n{actual_lines}"

def test_no_tmp_files_left():
    # Ensure no .tmp files are left in the clean dataset directory
    for root, dirs, files in os.walk(CLEAN_DATASET_DIR):
        for file in files:
            assert not file.endswith(".tmp"), f"Temporary file {file} was left behind in {root}."