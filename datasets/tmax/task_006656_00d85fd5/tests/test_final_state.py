# test_final_state.py

import os
import json
import pytest
import re

def test_schema_errors_json():
    file_path = "/home/user/schema_errors.json"
    assert os.path.isfile(file_path), f"{file_path} is missing."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{file_path} is not a valid JSON file.")

    assert isinstance(data, list), f"{file_path} should contain a JSON array."

    expected_errors = {"job2", "job3"}
    actual_errors = set(data)

    assert actual_errors == expected_errors, f"Expected schema errors to be {expected_errors}, but got {actual_errors}."

def test_failed_s3_dbs_json():
    file_path = "/home/user/failed_s3_dbs.json"
    assert os.path.isfile(file_path), f"{file_path} is missing."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{file_path} is not a valid JSON file.")

    assert isinstance(data, list), f"{file_path} should contain a JSON array."

    expected_dbs = {"prod-db-1"}
    actual_dbs = set(data)

    assert actual_dbs == expected_dbs, f"Expected failed S3 DBs to be {expected_dbs}, but got {actual_dbs}."

def test_index_strategy_txt():
    file_path = "/home/user/index_strategy.txt"
    assert os.path.isfile(file_path), f"{file_path} is missing."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    # Normalize whitespace and case
    normalized_content = re.sub(r'\s+', ' ', content).strip(';').lower()

    expected_patterns = [
        r"create index for \(b:backupjob\) on \(b\.status\)",
        r"create index on :backupjob\(status\)"
    ]

    matched = any(re.match(pattern, normalized_content) for pattern in expected_patterns)
    assert matched, f"The Cypher query in {file_path} is not a valid index creation statement for BackupJob.status. Got: {content}"