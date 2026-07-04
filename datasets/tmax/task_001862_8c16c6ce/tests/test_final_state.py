# test_final_state.py

import os
import json
import sys
import pytest

def test_results_json_exists_and_correct():
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"File not found: {results_path}"

    with open(results_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("results.json is not valid JSON")

    expected_results = {"1": True, "2": True, "3": True}
    assert results == expected_results, f"results.json does not match expected output. Got {results}, expected {expected_results}"

def test_algo_fixed():
    algo_path = "/home/user/algo.py"
    assert os.path.isfile(algo_path), f"File not found: {algo_path}"

    sys.path.insert(0, "/home/user")
    try:
        import algo
    except ImportError:
        pytest.fail("Could not import algo.py")

    try:
        # Test with a graph where the leaf node 'B' is not explicitly a key
        graph = {"A": [["B", 5]]}
        result = algo.longest_path(graph, "A")
        assert result == 5, f"Expected longest_path to return 5, but got {result}"
    except KeyError as e:
        pytest.fail(f"algo.longest_path raised KeyError: {e}. The bug is not fixed.")
    except Exception as e:
        pytest.fail(f"algo.longest_path raised an unexpected exception: {e}")