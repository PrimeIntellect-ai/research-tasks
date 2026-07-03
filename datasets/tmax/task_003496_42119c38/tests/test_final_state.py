# test_final_state.py
import json
import os
import pytest

def test_optimized_results_exists():
    file_path = "/home/user/optimized_results.json"
    assert os.path.isfile(file_path), f"The output file {file_path} is missing."

def test_optimized_results_content():
    file_path = "/home/user/optimized_results.json"

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {file_path} is not valid JSON.")
    except Exception as e:
        pytest.fail(f"Could not read {file_path}: {e}")

    expected_in_degree = ["user_1", "user_5", "user_9", "user_2", "user_3"]
    expected_pagerank = ["user_1", "user_5", "user_4", "user_9", "user_2"]

    assert "top_in_degree" in data, "The key 'top_in_degree' is missing from the JSON output."
    assert "top_pagerank" in data, "The key 'top_pagerank' is missing from the JSON output."

    assert data["top_in_degree"] == expected_in_degree, (
        f"Incorrect 'top_in_degree'. Expected {expected_in_degree}, got {data['top_in_degree']}"
    )

    assert data["top_pagerank"] == expected_pagerank, (
        f"Incorrect 'top_pagerank'. Expected {expected_pagerank}, got {data['top_pagerank']}"
    )