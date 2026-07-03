# test_final_state.py

import os
import json
import pytest

ANALYZE_SCRIPT = "/home/user/analyze.sh"
TOP_PAPERS_FILE = "/home/user/top_papers.json"

def test_analyze_script_exists():
    assert os.path.isfile(ANALYZE_SCRIPT), f"The script '{ANALYZE_SCRIPT}' does not exist."

def test_top_papers_file_exists():
    assert os.path.isfile(TOP_PAPERS_FILE), f"The output file '{TOP_PAPERS_FILE}' was not generated."

def test_top_papers_content():
    assert os.path.isfile(TOP_PAPERS_FILE), f"The output file '{TOP_PAPERS_FILE}' is missing."

    try:
        with open(TOP_PAPERS_FILE, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file '{TOP_PAPERS_FILE}' does not contain valid JSON.")

    expected_data = [
        {
            "id": "P1",
            "citing_institutions_count": 3
        },
        {
            "id": "P2",
            "citing_institutions_count": 2
        },
        {
            "id": "P3",
            "citing_institutions_count": 2
        }
    ]

    assert isinstance(data, list), f"The root of '{TOP_PAPERS_FILE}' must be a JSON array."
    assert len(data) == 3, f"Expected exactly 3 results in '{TOP_PAPERS_FILE}', but found {len(data)}."

    for i, expected_item in enumerate(expected_data):
        assert data[i] == expected_item, (
            f"Mismatch at index {i} in '{TOP_PAPERS_FILE}'. "
            f"Expected: {expected_item}, Got: {data[i]}"
        )