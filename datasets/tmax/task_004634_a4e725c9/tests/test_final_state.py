# test_final_state.py
import os
import json
import pytest

def test_analyzer_go_exists():
    """Verify that the Go analyzer script exists."""
    file_path = "/home/user/analyzer.go"
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did you write the Go program?"

def test_summary_json_exists():
    """Verify that the summary.json file was generated."""
    file_path = "/home/user/summary.json"
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did you run the Go program to generate the output?"

def test_summary_json_content():
    """Verify the contents of summary.json match the expected aggregation."""
    file_path = "/home/user/summary.json"

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {file_path} as JSON: {e}")

    assert isinstance(data, dict), f"Expected the JSON root to be an object, but got {type(data).__name__}."

    expected = {
        "Alice": 3,
        "Bob": 1,
        "Charlie": 2
    }

    assert data.get("Alice") == 3, f"Expected Alice to have 3 changes, got {data.get('Alice')}."
    assert data.get("Bob") == 1, f"Expected Bob to have 1 change, got {data.get('Bob')}."
    assert data.get("Charlie") == 2, f"Expected Charlie to have 2 changes, got {data.get('Charlie')}."

    assert "Eve" not in data, "Found 'Eve' in the summary, but her backup had an invalid checksum and should have been skipped."

    # Check for exact match
    assert data == expected, f"Summary JSON does not match expected output. Expected {expected}, got {data}."