# test_final_state.py

import os
import csv
import hashlib
import pytest

RAW_DATA_DIR = "/home/user/raw_data"
CLEAN_DATA_DIR = "/home/user/clean_data"
SCRIPT_PATH = "/home/user/clean_pipeline.sh"
CHECKSUMS_PATH = "/home/user/checksums.txt"

def get_expected_clean_data(raw_filepath):
    """Derive the expected cleaned data from the raw file based on task rules."""
    expected_lines = []
    with open(raw_filepath, 'r', newline='') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
            expected_lines.append(",".join(header[:3]))
        except StopIteration:
            return ""

        for row in reader:
            if len(row) < 5:
                continue
            temperature = row[2]
            status = row[4]

            if status == 'ERROR':
                continue
            if temperature == '999.9':
                continue

            expected_lines.append(",".join(row[:3]))

    return "\n".join(expected_lines) + "\n"

def test_script_exists():
    """Check if the bash script was created at the specified path."""
    assert os.path.isfile(SCRIPT_PATH), f"Script file not found at {SCRIPT_PATH}"

def test_clean_data_directory_exists():
    """Check if the clean_data directory was created."""
    assert os.path.isdir(CLEAN_DATA_DIR), f"Directory {CLEAN_DATA_DIR} does not exist."

def test_cleaned_csv_files_content():
    """Check if the cleaned CSV files match the expected output derived from raw data."""
    raw_files = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith('.csv')]
    assert len(raw_files) > 0, f"No raw CSV files found in {RAW_DATA_DIR} to process."

    for filename in raw_files:
        raw_filepath = os.path.join(RAW_DATA_DIR, filename)
        clean_filepath = os.path.join(CLEAN_DATA_DIR, filename)

        assert os.path.isfile(clean_filepath), f"Cleaned file {filename} is missing in {CLEAN_DATA_DIR}."

        expected_content = get_expected_clean_data(raw_filepath)

        with open(clean_filepath, 'r', newline='') as f:
            actual_content = f.read()

        # Strip trailing newlines for robust comparison
        assert actual_content.strip() == expected_content.strip(), (
            f"Content of {clean_filepath} does not match expected cleaned data.\n"
            f"Expected:\n{expected_content.strip()}\nGot:\n{actual_content.strip()}"
        )

def test_checksums_file():
    """Check if the checksums file exists and contains the correct SHA-256 hashes."""
    assert os.path.isfile(CHECKSUMS_PATH), f"Checksums file not found at {CHECKSUMS_PATH}"

    # Calculate actual hashes of files in clean_data
    actual_hashes = {}
    clean_files = [f for f in os.listdir(CLEAN_DATA_DIR) if f.endswith('.csv')]
    for filename in clean_files:
        filepath = os.path.join(CLEAN_DATA_DIR, filename)
        with open(filepath, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        actual_hashes[filepath] = file_hash

    # Parse the checksums.txt file
    with open(CHECKSUMS_PATH, 'r') as f:
        checksums_content = f.read().strip().splitlines()

    assert len(checksums_content) > 0, f"{CHECKSUMS_PATH} is empty."

    parsed_checksums = {}
    for line in checksums_content:
        parts = line.split()
        if len(parts) >= 2:
            hash_val = parts[0]
            # Handle potential asterisk for binary mode in sha256sum output
            file_path = parts[1].lstrip('*')
            parsed_checksums[file_path] = hash_val

    # Verify that all cleaned files are in the checksums file and hashes match
    for filepath, expected_hash in actual_hashes.items():
        # The checksum file might use absolute paths or relative paths depending on how it was run.
        # We will check if the filename or absolute path is present and matches.
        matched = False
        for parsed_path, parsed_hash in parsed_checksums.items():
            if parsed_path == filepath or parsed_path == os.path.basename(filepath) or parsed_path.endswith(filepath):
                assert parsed_hash == expected_hash, f"Hash mismatch for {filepath} in {CHECKSUMS_PATH}. Expected {expected_hash}, got {parsed_hash}."
                matched = True
                break
        assert matched, f"File {filepath} (or its basename) not found in {CHECKSUMS_PATH}."