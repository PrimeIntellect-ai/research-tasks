# test_final_state.py

import os
import json
import pytest

def test_results_file_exists():
    """Check if the top_matches.json file exists in the correct directory."""
    file_path = "/home/user/results/top_matches.json"
    assert os.path.isfile(file_path), f"Expected output file {file_path} is missing."

def test_results_content():
    """Check if the top_matches.json contains the correct query and top 3 files."""
    file_path = "/home/user/results/top_matches.json"
    assert os.path.isfile(file_path), f"Cannot check content, {file_path} is missing."

    with open(file_path, 'r') as f:
        try:
            result = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not a valid JSON.")

    expected_query = "Medical chest X-ray images for pneumonia detection and classification"
    expected_files = ["dataset_01.txt", "dataset_08.txt", "dataset_03.txt"]

    assert "query" in result, "JSON missing 'query' key."
    assert "top_3_files" in result, "JSON missing 'top_3_files' key."

    assert result["query"] == expected_query, f"Expected query '{expected_query}', but got '{result['query']}'."
    assert result["top_3_files"] == expected_files, f"Expected top_3_files to be {expected_files}, but got {result['top_3_files']}."