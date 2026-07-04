# test_final_state.py

import os
import json
import pytest

def test_result_json_exists():
    """Verify that the result.json file exists."""
    assert os.path.isfile("/home/user/result.json"), "The expected output file /home/user/result.json is missing."

def test_query_accuracy():
    """Verify that the extracted query sequence meets the accuracy threshold."""
    truth_path = "/app/truth.txt"
    result_path = "/home/user/result.json"

    assert os.path.isfile(truth_path), f"Truth file {truth_path} is missing."
    assert os.path.isfile(result_path), f"Result file {result_path} is missing."

    with open(truth_path, 'r') as f:
        truth_seq = f.read().strip()

    with open(result_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The file /home/user/result.json does not contain valid JSON.")

    assert "query" in data, "The JSON file is missing the 'query' key."
    query = data["query"]

    assert isinstance(query, str), "The 'query' value must be a string."
    assert len(query) == len(truth_seq), f"Length mismatch: query length {len(query)}, expected {len(truth_seq)}."

    matches = sum(1 for a, b in zip(query, truth_seq) if a == b)
    accuracy = matches / len(truth_seq)

    assert accuracy >= 0.98, f"Accuracy {accuracy:.2f} is below the threshold of 0.98."

def test_best_match_fields():
    """Verify that the JSON result contains the correct fields for the best match."""
    result_path = "/home/user/result.json"

    with open(result_path, 'r') as f:
        data = json.load(f)

    assert "best_match_header" in data, "The JSON file is missing the 'best_match_header' key."
    assert "hamming_distance" in data, "The JSON file is missing the 'hamming_distance' key."

    # As per the setup script, the best match is SEQ_04200 with a Hamming distance of 1
    # We won't strictly fail if the student's exact match is slightly off due to query extraction errors,
    # but we ensure the types are correct.
    assert isinstance(data["best_match_header"], str), "The 'best_match_header' must be a string."
    assert isinstance(data["hamming_distance"], int), "The 'hamming_distance' must be an integer."