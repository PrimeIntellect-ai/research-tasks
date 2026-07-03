# test_final_state.py

import json
import os
import pytest

def test_clean_reviews_jsonl_exists():
    file_path = "/home/user/clean_reviews.jsonl"
    assert os.path.exists(file_path), f"The output file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a regular file."

def test_clean_reviews_jsonl_content():
    file_path = "/home/user/clean_reviews.jsonl"

    expected = [
        {"id": "A1B2C3D4", "lang": "en", "score": 5, "content": "Great product!"},
        {"id": "A1B2C3D7", "lang": "es", "score": 4, "content": "Me gusta \ufffd el producto"},
        {"id": "A1B2C3D8", "lang": "fr", "score": 3, "content": "Très bien"},
        {"id": "X9Y8Z7W6", "lang": "ko", "score": 2, "content": "각"}
    ]

    actual = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                parsed = json.loads(line)
                actual.append(parsed)
            except json.JSONDecodeError as e:
                pytest.fail(f"Invalid JSON on line {line_num} of {file_path}: {e}")

    assert len(actual) == len(expected), f"Expected {len(expected)} records in the output, but got {len(actual)}."

    for i, (act, exp) in enumerate(zip(actual, expected)):
        assert act == exp, f"Record mismatch at index {i}.\nExpected: {exp}\nGot: {act}"