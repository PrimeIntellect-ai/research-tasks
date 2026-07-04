# test_final_state.py
import os
import json
import pytest

def test_graph_index_exists_and_valid():
    index_path = "/home/user/graph_index.json"
    assert os.path.exists(index_path), f"File missing: {index_path}"
    assert os.path.isfile(index_path), f"Path is not a file: {index_path}"

    with open(index_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {index_path} is not valid JSON")

    assert isinstance(data, dict), f"Root of {index_path} must be a JSON object"
    assert "Raw_Alpha" in data, f"'Raw_Alpha' key missing in {index_path}"

    # Check structure of Raw_Alpha
    raw_alpha_edges = data["Raw_Alpha"]
    assert isinstance(raw_alpha_edges, list), "Value for 'Raw_Alpha' must be an array"
    if len(raw_alpha_edges) > 0:
        edge = raw_alpha_edges[0]
        assert "target" in edge, "Edge object missing 'target' key"
        assert "cost" in edge, "Edge object missing 'cost' key"

def test_path_result_exists_and_correct():
    result_path = "/home/user/path_result.json"
    assert os.path.exists(result_path), f"File missing: {result_path}"
    assert os.path.isfile(result_path), f"Path is not a file: {result_path}"

    with open(result_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {result_path} is not valid JSON")

    assert data.get("source") == "Raw_Alpha", f"Expected source to be 'Raw_Alpha', got {data.get('source')}"
    assert data.get("target") == "Final_Omega", f"Expected target to be 'Final_Omega', got {data.get('target')}"
    assert data.get("total_time_hours") == 5, f"Expected total_time_hours to be 5, got {data.get('total_time_hours')}"

    expected_path = ["Raw_Alpha", "Clean_Alpha", "Fast_Track", "Final_Omega"]
    assert data.get("path") == expected_path, f"Expected path {expected_path}, got {data.get('path')}"