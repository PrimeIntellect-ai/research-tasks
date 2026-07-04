# test_final_state.py
import os
import pytest

PROCESSED_DIR = "/home/user/processed_backups"
RAW_DIR = "/home/user/raw_backups"
AUDIT_LOG_PATH = "/home/user/audit_log.txt"

def test_processed_dir_exists():
    assert os.path.exists(PROCESSED_DIR), f"Processed directory {PROCESSED_DIR} does not exist."
    assert os.path.isdir(PROCESSED_DIR), f"{PROCESSED_DIR} is not a directory."

def test_processed_files_count_and_names():
    assert os.path.exists(PROCESSED_DIR), "Processed directory missing."
    processed_files = sorted(os.listdir(PROCESSED_DIR))

    # Filter out any lingering temporary files
    actual_files = [f for f in processed_files if not f.startswith('.tmp')]

    assert len(actual_files) == 50, f"Expected 50 processed files, found {len(actual_files)}"

    for i, filename in enumerate(actual_files):
        expected_name = f"archive_{i+1:03d}.dat"
        assert filename == expected_name, f"Expected file {expected_name}, but found {filename}"

def test_audit_log_exists_and_content():
    assert os.path.exists(AUDIT_LOG_PATH), f"Audit log {AUDIT_LOG_PATH} does not exist."
    assert os.path.isfile(AUDIT_LOG_PATH), f"{AUDIT_LOG_PATH} is not a file."

    with open(AUDIT_LOG_PATH, 'r') as f:
        audit_lines = [line.strip() for line in f if line.strip()]

    assert len(audit_lines) == 50, f"Audit log does not have exactly 50 lines. Found {len(audit_lines)}."

    raw_files = sorted(os.listdir(RAW_DIR))
    for i, line in enumerate(audit_lines):
        expected_line = f"{raw_files[i]} -> archive_{i+1:03d}.dat"
        assert line == expected_line, f"Audit log mismatch at line {i+1}. Expected: '{expected_line}', Got: '{line}'"

def test_file_sanitization():
    assert os.path.exists(PROCESSED_DIR), "Processed directory missing."
    processed_files = sorted([f for f in os.listdir(PROCESSED_DIR) if not f.startswith('.tmp')])
    assert len(processed_files) == 50, "Expected 50 processed files to check."

    for filename in processed_files:
        filepath = os.path.join(PROCESSED_DIR, filename)
        with open(filepath, 'rb') as f:
            content = f.read()

            assert b"SECRET_TOKEN:" not in content, f"Found unredacted SECRET_TOKEN in {filename}"
            assert b"REDACTED_KEY:00000000" in content, f"No redacted keys found in {filename}, meaning replacement failed."

def test_raw_files_untouched():
    assert os.path.exists(RAW_DIR), "Raw directory missing."
    raw_files = os.listdir(RAW_DIR)
    assert len(raw_files) == 50, "Original raw files were deleted or modified in count."