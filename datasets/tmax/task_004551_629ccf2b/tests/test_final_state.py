# test_final_state.py

import os
import json
import pytest

def test_clean_features_jsonl():
    file_path = "/home/user/clean_features.jsonl"
    assert os.path.exists(file_path), f"Expected output file {file_path} is missing."

    expected_records = [
        {"user_id": "u1", "clean_text": "great product highly recommend", "word_count": 4, "rolling_avg_3": 4.00},
        {"user_id": "u2", "clean_text": "terrible service wont buy again", "word_count": 5, "rolling_avg_3": 4.50},
        {"user_id": "u3", "clean_text": "okay but 100 too expensive", "word_count": 5, "rolling_avg_3": 4.67},
        {"user_id": "u4", "clean_text": "i love it", "word_count": 3, "rolling_avg_3": 4.33},
        {"user_id": "u5", "clean_text": "wait what", "word_count": 2, "rolling_avg_3": 3.33},
        {"user_id": "u6", "clean_text": "multiple spaces here", "word_count": 3, "rolling_avg_3": 2.67}
    ]

    actual_records = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                actual_records.append(record)
            except json.JSONDecodeError:
                pytest.fail(f"Line {line_num} in {file_path} is not valid JSON: {line}")

    assert len(actual_records) == len(expected_records), f"Expected {len(expected_records)} records, but found {len(actual_records)}."

    for i, (actual, expected) in enumerate(zip(actual_records, expected_records)):
        assert actual.get("user_id") == expected["user_id"], f"Record {i+1} user_id mismatch. Expected {expected['user_id']}, got {actual.get('user_id')}"
        assert actual.get("clean_text") == expected["clean_text"], f"Record {i+1} clean_text mismatch. Expected '{expected['clean_text']}', got '{actual.get('clean_text')}'"
        assert actual.get("word_count") == expected["word_count"], f"Record {i+1} word_count mismatch. Expected {expected['word_count']}, got {actual.get('word_count')}"

        # Check rolling average with tolerance for float parsing, but also check string representation if possible.
        # The prompt says "exactly formatted to 2 decimal places", but in parsed JSON it's a float.
        # We will check if it's close to the expected float.
        actual_avg = actual.get("rolling_avg_3")
        assert actual_avg is not None, f"Record {i+1} is missing 'rolling_avg_3'"
        assert isinstance(actual_avg, (int, float)), f"Record {i+1} 'rolling_avg_3' must be a number"
        assert abs(actual_avg - expected["rolling_avg_3"]) < 0.005, f"Record {i+1} rolling_avg_3 mismatch. Expected {expected['rolling_avg_3']}, got {actual_avg}"

    # Also check the exact string formatting of rolling_avg_3 in the file
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
        for i, line in enumerate(lines):
            # A simple check to ensure the value has two decimal places
            expected_str = f"{expected_records[i]['rolling_avg_3']:.2f}"
            assert expected_str in line, f"Record {i+1} does not appear to have 'rolling_avg_3' formatted to exactly 2 decimal places. Expected to find '{expected_str}' in line."

def test_pipeline_log():
    file_path = "/home/user/pipeline.log"
    assert os.path.exists(file_path), f"Expected log file {file_path} is missing."

    expected_log = "[INFO] Processed 6 valid records. Skipped 2 duplicate records."

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    assert content == expected_log, f"Log file content mismatch. Expected '{expected_log}', got '{content}'"