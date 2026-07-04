# test_final_state.py

import os
import json
import re
import pytest
from pathlib import Path

OUTPUT_FILE = "/home/user/cleaned_sampled.jsonl"
RAW_DATA_DIR = "/home/user/raw_data"

def compute_expected_data():
    raw_records = []
    raw_dir = Path(RAW_DATA_DIR)

    if not raw_dir.exists():
        return {}

    # Read all raw data
    for file_path in raw_dir.glob("*.jsonl"):
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    raw_records.append(json.loads(line))

    # Process records
    valid_records_by_category = {}
    for record in raw_records:
        text = record.get("text", "")
        # Lowercase
        text = text.lower()
        # Remove all characters EXCEPT alphanumeric and spaces
        text = re.sub(r'[^a-z0-9 ]', '', text)
        # Replace multiple spaces with single space and strip
        text = re.sub(r' +', ' ', text).strip()

        # Tokenize
        tokens = text.split(' ') if text else []
        token_count = len(tokens)

        # Filter
        if token_count >= 3:
            cat = record["category"]
            if cat not in valid_records_by_category:
                valid_records_by_category[cat] = []

            valid_records_by_category[cat].append({
                "id": record["id"],
                "category": cat,
                "normalized_text": text,
                "token_count": token_count
            })

    # Stratify and select
    expected_output = {}
    for cat, records in valid_records_by_category.items():
        # Sort alphabetically by id
        records.sort(key=lambda x: x["id"])
        # Select first 5
        selected = records[:5]
        for rec in selected:
            expected_output[rec["id"]] = rec

    return expected_output

def test_output_file_exists():
    """Ensure the cleaned sampled dataset file was created."""
    assert os.path.exists(OUTPUT_FILE), f"Expected output file {OUTPUT_FILE} does not exist."
    assert os.path.isfile(OUTPUT_FILE), f"{OUTPUT_FILE} is not a file."

def test_output_file_contents():
    """Verify the contents of the output file match the expected processed data."""
    assert os.path.exists(OUTPUT_FILE), f"Cannot verify contents, {OUTPUT_FILE} is missing."

    expected_data = compute_expected_data()
    assert expected_data, "Expected data could not be computed (raw data might be missing)."

    actual_data = {}
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as e:
                pytest.fail(f"Invalid JSON on line {line_num} in {OUTPUT_FILE}: {e}")

            assert "id" in record, f"Record on line {line_num} is missing the 'id' field."
            actual_data[record["id"]] = record

    # Check total count
    expected_count = len(expected_data)
    actual_count = len(actual_data)
    assert actual_count == expected_count, (
        f"Expected exactly {expected_count} records, but found {actual_count}."
    )

    # Check each expected record
    for expected_id, expected_record in expected_data.items():
        assert expected_id in actual_data, f"Expected record with id '{expected_id}' is missing from the output."

        actual_record = actual_data[expected_id]

        # Check exact keys
        expected_keys = {"id", "category", "normalized_text", "token_count"}
        actual_keys = set(actual_record.keys())
        assert actual_keys == expected_keys, (
            f"Record {expected_id} has incorrect keys. Expected {expected_keys}, got {actual_keys}."
        )

        # Check values
        assert actual_record["category"] == expected_record["category"], (
            f"Record {expected_id} has wrong category. Expected '{expected_record['category']}', got '{actual_record['category']}'."
        )
        assert actual_record["normalized_text"] == expected_record["normalized_text"], (
            f"Record {expected_id} has wrong normalized_text. Expected '{expected_record['normalized_text']}', got '{actual_record['normalized_text']}'."
        )
        assert actual_record["token_count"] == expected_record["token_count"], (
            f"Record {expected_id} has wrong token_count. Expected {expected_record['token_count']}, got {actual_record['token_count']}."
        )