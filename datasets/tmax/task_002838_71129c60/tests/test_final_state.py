# test_final_state.py

import os
import json
import pytest

def test_anomalies_sampled_json():
    output_file = "/home/user/anomalies_sampled.json"

    assert os.path.exists(output_file), f"Output file {output_file} does not exist."
    assert os.path.isfile(output_file), f"Path {output_file} is not a file."

    try:
        with open(output_file, "r", encoding="utf-8") as f:
            actual_data = json.load(f)
    except json.JSONDecodeError as e:
        pytest.fail(f"File {output_file} is not valid JSON: {e}")

    expected_data = [
        {"timestamp_sec": 104, "language": "en", "content": "Wow that is a lot"},
        {"timestamp_sec": 102, "language": "en", "content": "A"},
        {"timestamp_sec": 102, "language": "fr", "content": "Bonjour"},
        {"timestamp_sec": 102, "language": "fr", "content": "Oui"},
        {"timestamp_sec": 102, "language": "ja", "content": "こんにちは"},
        {"timestamp_sec": 102, "language": "ja", "content": "はい"},
        {"timestamp_sec": 104, "language": "zh", "content": "工程师"},
        {"timestamp_sec": 104, "language": "zh", "content": "世界"}
    ]

    assert isinstance(actual_data, list), f"Expected JSON array, got {type(actual_data).__name__}."
    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} items, got {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual == expected, f"Mismatch at index {i}. Expected {expected}, got {actual}."