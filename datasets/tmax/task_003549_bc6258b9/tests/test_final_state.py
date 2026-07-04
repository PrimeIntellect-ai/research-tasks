# test_final_state.py

import os
import json
import pytest

def test_pipeline_exists_and_executable():
    """Check if the pipeline script exists and is executable."""
    pipeline_path = "/home/user/pipeline.sh"
    assert os.path.isfile(pipeline_path), f"Pipeline script {pipeline_path} does not exist."
    assert os.access(pipeline_path, os.X_OK), f"Pipeline script {pipeline_path} is not executable."

def test_result_json_exists():
    """Check if the result JSON file exists."""
    result_path = "/home/user/output/result.json"
    assert os.path.isfile(result_path), f"Result file {result_path} does not exist."

def test_result_json_content():
    """Check if the result JSON file contains the correct optimal k and top 3 items."""
    result_path = "/home/user/output/result.json"
    assert os.path.isfile(result_path), f"Result file {result_path} does not exist."

    with open(result_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {result_path} is not valid JSON.")

    assert "optimal_k" in data, "Key 'optimal_k' missing from result JSON."
    assert "item_0_top_3" in data, "Key 'item_0_top_3' missing from result JSON."
    assert "item_5_top_3" in data, "Key 'item_5_top_3' missing from result JSON."

    expected_k = 5
    expected_item_0 = [11, 4, 3]
    expected_item_5 = [14, 6, 2]

    assert data["optimal_k"] == expected_k, f"Expected optimal_k to be {expected_k}, got {data['optimal_k']}"
    assert data["item_0_top_3"] == expected_item_0, f"Expected item_0_top_3 to be {expected_item_0}, got {data['item_0_top_3']}"
    assert data["item_5_top_3"] == expected_item_5, f"Expected item_5_top_3 to be {expected_item_5}, got {data['item_5_top_3']}"