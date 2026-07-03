# test_final_state.py

import os
import json
import gzip
import pytest

BASE_DIR = "/home/user/storage_pool"
AUDIT_LOG = "/home/user/audit_log.jsonl"

def test_audit_log_exists():
    """Verify that the central audit log was created."""
    assert os.path.exists(AUDIT_LOG), f"Audit log missing at {AUDIT_LOG}"
    assert os.path.isfile(AUDIT_LOG), f"{AUDIT_LOG} is not a file"

def test_unlocked_vlogs_deleted_and_locked_vlogs_skipped():
    """Ensure no .vlog files exist unless they have a corresponding .lock file."""
    assert os.path.exists(BASE_DIR), f"Base directory {BASE_DIR} is missing."
    for root, dirs, files in os.walk(BASE_DIR):
        for f in files:
            if f.endswith(".vlog"):
                lock_file = f + ".lock"
                assert lock_file in files, (
                    f"Found unlocked vlog file that was not deleted: {os.path.join(root, f)}"
                )

def test_jsonl_gz_format_and_content():
    """Verify that converted files are valid gzipped JSONL with the correct keys."""
    gz_files = []
    for root, dirs, files in os.walk(BASE_DIR):
        for f in files:
            if f.endswith(".jsonl.gz"):
                gz_files.append(os.path.join(root, f))

    assert len(gz_files) > 0, "No .jsonl.gz files found. No files appear to have been converted."

    expected_keys = {"level", "timestamp", "user", "action", "status"}
    for path in gz_files:
        try:
            with gzip.open(path, 'rt') as gz:
                lines = gz.readlines()
        except Exception as e:
            pytest.fail(f"Failed to read {path} as a gzip file: {e}")

        if lines:
            try:
                obj = json.loads(lines[0])
            except json.JSONDecodeError:
                pytest.fail(f"First line of {path} is not valid JSON.")

            assert expected_keys.issubset(obj.keys()), (
                f"Missing keys in JSON object in {path}. Expected {expected_keys}, found: {set(obj.keys())}"
            )

def test_audit_log_matches_conversions():
    """Verify the audit log contains correct entries that match the filesystem state."""
    assert os.path.exists(AUDIT_LOG), "Audit log missing"

    processed_count = 0
    with open(AUDIT_LOG, 'r') as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                pytest.fail(f"Audit log line {line_num} is not valid JSON: {line}")

            orig_file = data.get('original_file')
            comp_file = data.get('compressed_file')
            lines_proc = data.get('lines_processed')

            assert orig_file, f"Audit log entry at line {line_num} missing 'original_file'"
            assert comp_file, f"Audit log entry at line {line_num} missing 'compressed_file'"
            assert lines_proc is not None, f"Audit log entry at line {line_num} missing 'lines_processed'"

            assert os.path.isabs(orig_file), f"'original_file' path must be absolute: {orig_file}"
            assert os.path.isabs(comp_file), f"'compressed_file' path must be absolute: {comp_file}"

            assert os.path.exists(comp_file), f"Compressed file recorded in audit log is missing: {comp_file}"
            assert not os.path.exists(orig_file), f"Original file recorded in audit log was not deleted: {orig_file}"

            try:
                with gzip.open(comp_file, 'rt') as gz:
                    actual_lines = len(gz.readlines())
            except Exception as e:
                pytest.fail(f"Failed to read compressed file {comp_file}: {e}")

            assert actual_lines == lines_proc, (
                f"Lines processed mismatch for {comp_file}: audit log says {lines_proc}, file has {actual_lines}"
            )
            processed_count += 1

    assert processed_count > 0, "Audit log is empty or no files were processed."