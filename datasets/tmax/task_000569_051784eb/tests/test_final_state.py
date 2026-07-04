# test_final_state.py

import os
import tarfile
import tempfile
import pytest

SCRIPT_PATH = "/home/user/process_matrices.sh"
ARCHIVE_PATH = "/home/user/archive.tar.gz"

EXPECTED_SUMMARY = [
    "matrix_2.csv: 25.12",
    "matrix_4.csv: 30.50"
]

EXPECTED_FILES = ["matrix_2.csv", "matrix_4.csv", "summary.log"]
UNEXPECTED_FILES = ["matrix_1.csv", "matrix_3.csv"]

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_archive_exists():
    assert os.path.isfile(ARCHIVE_PATH), f"Archive {ARCHIVE_PATH} does not exist."
    assert tarfile.is_tarfile(ARCHIVE_PATH), f"File {ARCHIVE_PATH} is not a valid tar archive."

def test_archive_contents():
    with tempfile.TemporaryDirectory() as temp_dir:
        with tarfile.open(ARCHIVE_PATH, "r:gz") as tar:
            tar.extractall(path=temp_dir)

        # Find the processed directory or where the files are extracted
        # The prompt says it should extract to `processed/...` or `home/user/data/processed/...`
        # We can just walk the extracted directory to find summary.log
        summary_log_path = None
        for root, dirs, files in os.walk(temp_dir):
            if "summary.log" in files:
                summary_log_path = os.path.join(root, "summary.log")
                break

        assert summary_log_path is not None, "summary.log not found in the extracted archive."

        processed_dir = os.path.dirname(summary_log_path)

        # Check summary.log contents
        with open(summary_log_path, "r") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        assert lines == EXPECTED_SUMMARY, f"summary.log contents incorrect. Expected {EXPECTED_SUMMARY}, got {lines}"

        # Check files in processed directory
        extracted_files = set(os.listdir(processed_dir))

        for expected_file in EXPECTED_FILES:
            assert expected_file in extracted_files, f"Expected file {expected_file} not found in archive."

        for unexpected_file in UNEXPECTED_FILES:
            assert unexpected_file not in extracted_files, f"Unexpected file {unexpected_file} found in archive."