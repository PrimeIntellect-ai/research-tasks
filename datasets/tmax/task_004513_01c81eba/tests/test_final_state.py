# test_final_state.py
import os
import pytest

def test_incoming_artifacts_empty():
    incoming_dir = "/home/user/incoming_artifacts"
    assert os.path.isdir(incoming_dir), f"Directory missing: {incoming_dir}"
    assert len(os.listdir(incoming_dir)) == 0, f"Directory {incoming_dir} should be empty"

def test_processed_artifacts():
    processed_dir = "/home/user/processed"
    assert os.path.isdir(processed_dir), f"Directory missing: {processed_dir}"
    expected_files = ["safe_app.tar.gz", "safe_data.zip"]
    for file in expected_files:
        filepath = os.path.join(processed_dir, file)
        assert os.path.isfile(filepath), f"File missing in processed: {filepath}"

def test_quarantine_artifacts():
    quarantine_dir = "/home/user/quarantine"
    assert os.path.isdir(quarantine_dir), f"Directory missing: {quarantine_dir}"
    expected_files = ["slip_tar.tar.gz", "slip_zip.zip", "bad_archive.tar.gz", "broken_data.zip"]
    for file in expected_files:
        filepath = os.path.join(quarantine_dir, file)
        assert os.path.isfile(filepath), f"File missing in quarantine: {filepath}"

def test_extracted_safe_artifacts():
    expected_paths = [
        "/home/user/safe_artifacts/safe_app/bin/run.sh",
        "/home/user/safe_artifacts/safe_data/data/info.txt"
    ]
    for path in expected_paths:
        assert os.path.isfile(path), f"Extracted file missing: {path}"

def test_artifact_audit_log():
    log_file = "/home/user/artifact_audit.log"
    assert os.path.isfile(log_file), f"Log file missing: {log_file}"

    with open(log_file, "r") as f:
        log_lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_entries = {
        "safe_app.tar.gz": "SAFE | N/A",
        "safe_data.zip": "SAFE | N/A",
        "slip_tar.tar.gz": "MALICIOUS | ../evil.sh",
        "slip_zip.zip": "MALICIOUS | /etc/shadow",
        "bad_archive.tar.gz": "CORRUPT | N/A",
        "broken_data.zip": "CORRUPT | N/A"
    }

    parsed_entries = {}
    for line in log_lines:
        parts = [p.strip() for p in line.split("|")]
        assert len(parts) == 3, f"Malformed log line: {line}"
        filename, status, detail = parts
        parsed_entries[filename] = f"{status} | {detail}"

    for filename, expected_status_detail in expected_entries.items():
        assert filename in parsed_entries, f"Missing log entry for {filename}"
        assert parsed_entries[filename] == expected_status_detail, f"Incorrect log entry for {filename}: expected {expected_status_detail}, got {parsed_entries[filename]}"