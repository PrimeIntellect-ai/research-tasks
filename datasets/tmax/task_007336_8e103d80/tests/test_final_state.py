# test_final_state.py
import os
import json
import pytest
import unicodedata

def test_go_file_exists_and_uses_goroutines():
    go_file_path = "/home/user/workspace/clean_data.go"
    assert os.path.isfile(go_file_path), f"Expected Go source file at {go_file_path} is missing."

    with open(go_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for the usage of goroutines
    assert "go " in content, "The Go program must use Goroutines (the 'go' keyword was not found)."

def test_output_jsonl_exists_and_correct():
    output_path = "/home/user/workspace/output.jsonl"
    assert os.path.isfile(output_path), f"Expected output file at {output_path} is missing."

    expected_records = [
        {"user_id": "1", "username": "alice_smith", "country": "UK", "normalized_review": "Good product!"},
        {"user_id": "2", "username": "taro_yamada", "country": "JPN", "normalized_review": "スゴイガ"},
        {"user_id": "3", "username": "helene_d", "country": "FRA", "normalized_review": "Très bien"},
        {"user_id": "4", "username": "ahmed_m", "country": "EGY", "normalized_review": "ممتاز"}
    ]

    # Ensure expected reviews are NFC normalized
    for rec in expected_records:
        rec["normalized_review"] = unicodedata.normalize("NFC", rec["normalized_review"])

    actual_records = []
    with open(output_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                actual_records.append(record)
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON line found in {output_path}: {line}")

    assert len(actual_records) == len(expected_records), f"Expected {len(expected_records)} records, but found {len(actual_records)}."

    # Check that actual records match expected records exactly (order independent)
    for expected in expected_records:
        assert expected in actual_records, f"Expected record {expected} not found in output.jsonl. Make sure the text is NFC normalized."

    # Also explicitly assert that the output strings are actually NFC normalized
    for actual in actual_records:
        review = actual.get("normalized_review", "")
        assert review == unicodedata.normalize("NFC", review), f"Review text '{review}' is not NFC normalized."