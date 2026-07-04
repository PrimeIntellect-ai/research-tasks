# test_final_state.py

import os
import json
import pytest

OUTPUT_PATH = '/home/user/output.json'
EXTRACT_SCRIPT = '/home/user/extract.py'

def test_extract_script_exists():
    assert os.path.isfile(EXTRACT_SCRIPT), f"Extraction script {EXTRACT_SCRIPT} does not exist."

def test_output_json_exists():
    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} does not exist."

def test_output_json_content():
    with open(OUTPUT_PATH, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_PATH} does not contain valid JSON.")

    expected_data = [
        {
            "user_id": 1,
            "profile": {
                "name": "Alice",
                "email": "alice@example.com"
            },
            "top_purchases": [
                {
                    "purchase_id": 103,
                    "amount": 200.0,
                    "category": "furniture"
                },
                {
                    "purchase_id": 102,
                    "amount": 120.0,
                    "category": "electronics"
                }
            ]
        },
        {
            "user_id": 2,
            "profile": {
                "name": "Bob",
                "email": "bob@example.com"
            },
            "top_purchases": [
                {
                    "purchase_id": 106,
                    "amount": 60.0,
                    "category": "books"
                },
                {
                    "purchase_id": 105,
                    "amount": 60.0,
                    "category": "clothing"
                }
            ]
        }
    ]

    assert isinstance(data, list), "Output JSON must be a list of objects."
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} users in the output, but found {len(data)}."

    # Validate the data strictly matches the expected structure and content
    assert data == expected_data, "The generated JSON does not match the expected nested document structure or content."