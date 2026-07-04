# test_final_state.py

import os
import json
import pytest

def test_results_file_exists():
    assert os.path.isfile("/home/user/results.json"), "The output file /home/user/results.json does not exist."

def test_results_content():
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), "The output file /home/user/results.json does not exist."

    with open(results_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The output file /home/user/results.json is not valid JSON.")

    expected = [
        {
            "paper_a": "Graph AI",
            "paper_b": "Neural Nets",
            "researcher_a": "Alice",
            "researcher_b": "Bob"
        },
        {
            "paper_a": "Data Mining",
            "paper_b": "Graph AI",
            "researcher_a": "Alice",
            "researcher_b": "Alice"
        },
        {
            "paper_a": "Neural Nets",
            "paper_b": "Data Mining",
            "researcher_a": "Bob",
            "researcher_b": "Alice"
        },
        {
            "paper_a": "Neural Nets",
            "paper_b": "Data Mining",
            "researcher_a": "Bob",
            "researcher_b": "Charlie"
        },
        {
            "paper_a": "Data Mining",
            "paper_b": "Graph AI",
            "researcher_a": "Charlie",
            "researcher_b": "Alice"
        }
    ]

    assert isinstance(results, list), "The results must be a JSON array."
    assert len(results) == len(expected), f"Expected {len(expected)} results, but got {len(results)}."

    # Sort both just in case, though the prompt says it should be sorted
    # We will check exact match including sorting
    assert results == expected, "The results do not match the expected output exactly or are not sorted correctly."