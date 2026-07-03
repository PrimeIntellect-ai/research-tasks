# test_final_state.py

import os
import json
import pytest

MANIFEST_PATH = "/home/user/backup_manifest.jsonl"

def test_manifest_exists():
    assert os.path.exists(MANIFEST_PATH), f"The output file {MANIFEST_PATH} does not exist."
    assert os.path.isfile(MANIFEST_PATH), f"The path {MANIFEST_PATH} is not a file."

def test_manifest_is_utf8():
    try:
        with open(MANIFEST_PATH, 'rb') as f:
            content = f.read()
        content.decode('utf-8')
    except UnicodeDecodeError as e:
        pytest.fail(f"The file {MANIFEST_PATH} is not strictly UTF-8 encoded: {e}")

def test_manifest_content_and_format():
    expected_records = [
        {
            "filepath": "/home/user/artifact_repo/legacy_gamma/metadata.csv",
            "artifact_id": "gamma-legacy",
            "version": "0.9.9",
            "checksum": "sha1:111222333444"
        },
        {
            "filepath": "/home/user/artifact_repo/project_alpha/v1/metadata.json",
            "artifact_id": "alpha-core",
            "version": "1.0.4",
            "checksum": "sha256:abc123def456"
        },
        {
            "filepath": "/home/user/artifact_repo/project_beta/v2/metadata.xml",
            "artifact_id": "beta-utils-déjà",
            "version": "2.1.0",
            "checksum": "md5:9876543210"
        }
    ]

    records = []
    with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
        for i, line in enumerate(lines):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
                records.append(record)
            except json.JSONDecodeError as e:
                pytest.fail(f"Line {i+1} in {MANIFEST_PATH} is not valid JSON: {e}")

    assert len(records) == len(expected_records), (
        f"Expected {len(expected_records)} records in the manifest, but found {len(records)}."
    )

    # Check for required keys in all records
    for i, record in enumerate(records):
        for key in ["filepath", "artifact_id", "version", "checksum"]:
            assert key in record, f"Record {i+1} is missing required key: '{key}'"

    # Check that the list is sorted alphabetically by filepath
    filepaths = [r["filepath"] for r in records]
    assert filepaths == sorted(filepaths), "The output lines are not sorted alphabetically by the 'filepath' key."

    # Verify exact matches
    for expected in expected_records:
        assert expected in records, f"Expected record {expected} not found in the manifest."