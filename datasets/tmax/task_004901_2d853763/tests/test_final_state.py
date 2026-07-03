# test_final_state.py
import os
import json
import pytest

def test_binned_stats_exists():
    """Verify that the output JSON file was successfully created."""
    file_path = '/home/user/binned_stats.json'
    assert os.path.isfile(file_path), f"Output file {file_path} was not created. Did the script run successfully?"

def test_binned_stats_content():
    """Verify that the output JSON file contains the correctly calculated next-midnight bins."""
    file_path = '/home/user/binned_stats.json'

    # Expected result derived from the input CSV:
    # 2024-01-30 -> next midnight is 2024-01-31 (2 entries)
    # 2024-01-31 -> next midnight is 2024-02-01 (1 entry)
    # 2024-02-01 -> next midnight is 2024-02-02 (1 entry)
    # 2024-02-29 -> next midnight is 2024-03-01 (1 entry)
    expected_output = {
        "2024-01-31T00:00:00+00:00": 2,
        "2024-02-01T00:00:00+00:00": 1,
        "2024-02-02T00:00:00+00:00": 1,
        "2024-03-01T00:00:00+00:00": 1
    }

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {file_path} does not contain valid JSON.")

    assert data == expected_output, (
        f"The contents of {file_path} do not match the expected aggregated data. "
        f"Expected: {expected_output}, Got: {data}"
    )