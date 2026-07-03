# test_final_state.py

import os
import json
import pytest

def test_json_output_exists_and_valid():
    json_path = "/home/user/output/optimized_primers.json"
    assert os.path.isfile(json_path), f"Output JSON file {json_path} is missing. The Rust application may not have run successfully."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert isinstance(data, list), "JSON output should be a list of results."
    assert len(data) > 0, "JSON output list is empty."

    for i, item in enumerate(data):
        assert "sequence_id" in item, f"Item at index {i} is missing 'sequence_id'."
        assert "params" in item, f"Item at index {i} is missing 'params'."
        assert "final_score" in item, f"Item at index {i} is missing 'final_score'."
        assert isinstance(item["final_score"], (int, float)), f"'final_score' at index {i} must be a number."
        import math
        assert not math.isnan(item["final_score"]), f"'final_score' at index {i} is NaN, which means the numerical instability was not fixed."

def test_average_score_output():
    json_path = "/home/user/output/optimized_primers.json"
    txt_path = "/home/user/output/average_score.txt"

    assert os.path.isfile(json_path), f"Output JSON file {json_path} is missing."
    assert os.path.isfile(txt_path), f"Output text file {txt_path} is missing. Did you write the script to calculate the average score?"

    with open(json_path, "r") as f:
        data = json.load(f)

    scores = [item["final_score"] for item in data]
    expected_avg = sum(scores) / len(scores)
    expected_avg_rounded = round(expected_avg, 3)

    with open(txt_path, "r") as f:
        txt_content = f.read().strip()

    try:
        actual_avg = float(txt_content)
    except ValueError:
        pytest.fail(f"Content of {txt_path} is not a valid float: '{txt_content}'")

    assert round(actual_avg, 3) == expected_avg_rounded, f"Expected average score (rounded to 3 decimal places) to be {expected_avg_rounded}, but got {actual_avg} in {txt_path}"