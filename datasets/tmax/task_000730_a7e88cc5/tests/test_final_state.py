# test_final_state.py

import os
import json
import pytest

def test_extractor_script_exists():
    """Test that the extractor script exists."""
    extractor_path = "/home/user/extractor.py"
    assert os.path.isfile(extractor_path), f"Expected extractor script at {extractor_path} but it was not found."

def test_parsed_logs_accuracy():
    """Test that the parsed logs meet the accuracy threshold of >= 0.98."""
    parsed_logs_path = "/home/user/parsed_logs.jsonl"
    assert os.path.isfile(parsed_logs_path), f"Expected parsed logs file at {parsed_logs_path} but it was not found."

    EXPECTED_TOTAL = 100000
    valid_records = 0

    with open(parsed_logs_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                if 'timestamp_us' in record and 'severity' in record and 'message' in record:
                    valid_records += 1
            except json.JSONDecodeError:
                pass

    accuracy = valid_records / EXPECTED_TOTAL

    assert accuracy >= 0.98, (
        f"Extraction accuracy is too low. "
        f"Expected >= 0.98, but got {accuracy:.4f} "
        f"({valid_records} valid records out of {EXPECTED_TOTAL})."
    )

def test_parsed_logs_no_extra_records():
    """Ensure we don't have an impossible number of valid records."""
    parsed_logs_path = "/home/user/parsed_logs.jsonl"
    if not os.path.exists(parsed_logs_path):
        return

    EXPECTED_TOTAL = 100000
    valid_records = 0

    with open(parsed_logs_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                if 'timestamp_us' in record and 'severity' in record and 'message' in record:
                    valid_records += 1
            except json.JSONDecodeError:
                pass

    assert valid_records <= EXPECTED_TOTAL, (
        f"Found {valid_records} valid records, which is more than the expected total "
        f"of {EXPECTED_TOTAL} records generated."
    )