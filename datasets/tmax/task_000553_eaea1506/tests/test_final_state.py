# test_final_state.py

import os
import json
import re
import pytest

CLEANED_LOGS_PATH = "/home/user/cleaned_logs.json"

def process_text(text):
    """Recompute the expected text transformation based on the rules."""
    lines = text.split('\n')
    filtered_lines = [line for line in lines if not line.startswith("DEBUG: ")]
    joined = '\n'.join(filtered_lines)
    # Redact IPv4 addresses
    redacted = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '[REDACTED]', joined)
    return redacted

def test_cleaned_logs_exists():
    assert os.path.exists(CLEANED_LOGS_PATH), f"Output file {CLEANED_LOGS_PATH} is missing."
    assert os.path.isfile(CLEANED_LOGS_PATH), f"Output path {CLEANED_LOGS_PATH} is not a file."

def test_cleaned_logs_content():
    with open(CLEANED_LOGS_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {CLEANED_LOGS_PATH} does not contain valid JSON.")

    assert isinstance(data, list), "The JSON root must be an array."
    assert len(data) == 2, f"Expected exactly 2 items in the JSON array, found {len(data)}."

    # Map file paths to their contents for easy lookup
    files_found = {item.get("file"): item.get("contents") for item in data}

    # Check that the active file was skipped
    assert "server1/active.dat" not in files_found, "Active file server1/active.dat must be skipped and not included in the JSON."

    # Original payloads from the setup
    log1 = "INFO: User admin logged in from 192.168.1.100\nDEBUG: Connection latency 45ms\nWARN: Disk space low on 10.0.0.5\nINFO: Backup completed"
    log3 = "DEBUG: Init DB\nERROR: Failed to bind to 127.0.0.1\nINFO: Retrying..."

    # Derive expected contents
    expected_log1 = process_text(log1)
    expected_log3 = process_text(log3)

    # Verify the finished files are present
    assert "server1/auth.dat" in files_found, "Missing server1/auth.dat in the JSON output."
    assert "server2/deep/db.dat" in files_found, "Missing server2/deep/db.dat in the JSON output."

    # Assert contents match the derived expectations
    assert files_found["server1/auth.dat"] == expected_log1, "Contents for server1/auth.dat do not match expected filtered/redacted text."
    assert files_found["server2/deep/db.dat"] == expected_log3, "Contents for server2/deep/db.dat do not match expected filtered/redacted text."