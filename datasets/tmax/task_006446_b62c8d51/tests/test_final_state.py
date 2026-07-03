# test_final_state.py

import os
import json
import pytest

def test_clean_transcript_exists():
    path = "/home/user/clean_transcript.json"
    assert os.path.isfile(path), f"The output file {path} does not exist. Ensure your Rust program writes to this exact path."

def test_clean_transcript_content():
    path = "/home/user/clean_transcript.json"
    assert os.path.isfile(path), f"Cannot verify content: {path} is missing."

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        pytest.fail(f"The file {path} does not contain valid JSON. Error: {e}")

    assert isinstance(data, list), f"Expected a JSON array at the root, but found {type(data).__name__}."

    expected = [
        {"timestamp": "2023-11-01T14:05:00Z", "text": "Hello world! 🚀", "char_count": 14},
        {"timestamp": "2023-11-01T14:05:05Z", "text": "Bonjour le monde.", "char_count": 17},
        {"timestamp": "2023-11-01T14:05:10Z", "text": "مرحبا", "char_count": 5},
        {"timestamp": "2023-11-01T14:05:15Z", "text": "こんにちは", "char_count": 5}
    ]

    assert len(data) == len(expected), f"Expected {len(expected)} objects in the JSON array, but found {len(data)}. Check your deduplication and filtering logic."

    for i, (actual_obj, expected_obj) in enumerate(zip(data, expected)):
        assert isinstance(actual_obj, dict), f"Item at index {i} is not a JSON object."

        # Check keys
        actual_keys = set(actual_obj.keys())
        expected_keys = {"timestamp", "text", "char_count"}
        assert actual_keys == expected_keys, f"Item at index {i} has incorrect keys. Expected {expected_keys}, found {actual_keys}."

        # Check values
        assert actual_obj["timestamp"] == expected_obj["timestamp"], f"Item at index {i} has incorrect timestamp. Expected '{expected_obj['timestamp']}', found '{actual_obj['timestamp']}'."
        assert actual_obj["text"] == expected_obj["text"], f"Item at index {i} has incorrect text. Expected '{expected_obj['text']}', found '{actual_obj['text']}'. Ensure correct tag removal, trimming, and NFC normalization."
        assert actual_obj["char_count"] == expected_obj["char_count"], f"Item at index {i} has incorrect char_count. Expected {expected_obj['char_count']}, found {actual_obj['char_count']}."