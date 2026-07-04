# test_final_state.py

import os
import json
import pytest

OUTPUT_FILE = "/home/user/processed_sample.json"

EXPECTED_OUTPUT = {
    "tech": {
        "data01.txt": ["i", "love", "python", "programming"],
        "data03.txt": ["windows", "is", "an", "os", "linux", "is", "too"],
        "data05.txt": ["caf", "and", "python"]
    },
    "other": {
        "data02.txt": ["some", "random", "text"],
        "data04.txt": ["machine", "learning", "is", "fun"],
        "data06.txt": ["a", "ai", "bowl", "is", "good"]
    }
}

def test_output_file_exists():
    assert os.path.exists(OUTPUT_FILE), f"Output file {OUTPUT_FILE} is missing."
    assert os.path.isfile(OUTPUT_FILE), f"{OUTPUT_FILE} is not a file."

def test_output_file_content():
    assert os.path.exists(OUTPUT_FILE), f"Output file {OUTPUT_FILE} is missing."

    try:
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse {OUTPUT_FILE} as JSON: {e}")
    except Exception as e:
        pytest.fail(f"Error reading {OUTPUT_FILE}: {e}")

    # Check top-level keys
    assert set(data.keys()) == {"tech", "other"}, "The JSON output must have exactly two keys: 'tech' and 'other'."

    # Check tech category
    tech_data = data["tech"]
    expected_tech = EXPECTED_OUTPUT["tech"]
    assert set(tech_data.keys()) == set(expected_tech.keys()), f"Expected tech files {list(expected_tech.keys())}, but got {list(tech_data.keys())}."
    for filename, tokens in expected_tech.items():
        assert tech_data[filename] == tokens, f"Tokens for {filename} in 'tech' do not match expected."

    # Check other category
    other_data = data["other"]
    expected_other = EXPECTED_OUTPUT["other"]
    assert set(other_data.keys()) == set(expected_other.keys()), f"Expected other files {list(expected_other.keys())}, but got {list(other_data.keys())}."
    for filename, tokens in expected_other.items():
        assert other_data[filename] == tokens, f"Tokens for {filename} in 'other' do not match expected."

    # Final exact match just in case
    assert data == EXPECTED_OUTPUT, "The overall JSON structure does not match the expected output exactly."