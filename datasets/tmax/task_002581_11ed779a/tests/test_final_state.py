# test_final_state.py

import os
import json
import pytest

def test_cpp_file_exists():
    """Check if the C++ source file was created."""
    cpp_file = "/home/user/tokenizer_check.cpp"
    assert os.path.isfile(cpp_file), f"The C++ source file {cpp_file} is missing."

def test_json_output_exists():
    """Check if the JSON summary file was created."""
    json_file = "/home/user/artifacts/token_summary.json"
    assert os.path.isfile(json_file), f"The output JSON file {json_file} is missing."

def test_json_output_contents():
    """Check if the JSON summary file contains the correct token and file counts."""
    json_file = "/home/user/artifacts/token_summary.json"

    # Calculate the expected values dynamically based on the files present
    raw_data_dir = "/home/user/artifacts/raw_data"
    expected_files = 0
    expected_tokens = 0

    if os.path.isdir(raw_data_dir):
        for filename in os.listdir(raw_data_dir):
            if filename.endswith(".txt"):
                expected_files += 1
                filepath = os.path.join(raw_data_dir, filename)
                with open(filepath, 'r') as f:
                    content = f.read()
                    tokens = content.split()
                    expected_tokens += len(tokens)

    with open(json_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_file} does not contain valid JSON.")

    assert "total_tokens" in data, "The JSON output is missing the 'total_tokens' key."
    assert "num_files" in data, "The JSON output is missing the 'num_files' key."

    assert data["total_tokens"] == expected_tokens, f"Expected {expected_tokens} total_tokens, but got {data['total_tokens']}."
    assert data["num_files"] == expected_files, f"Expected {expected_files} num_files, but got {data['num_files']}."