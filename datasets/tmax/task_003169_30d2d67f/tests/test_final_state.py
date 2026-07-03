# test_final_state.py

import os
import json
import pytest

def test_results_json_exists():
    assert os.path.isfile("/home/user/results.json"), "The file /home/user/results.json does not exist."

def test_results_json_content():
    with open("/home/user/results.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The file /home/user/results.json does not contain valid JSON.")

    assert "vocab_size" in data, "The key 'vocab_size' is missing from results.json."
    assert "test_accuracy" in data, "The key 'test_accuracy' is missing from results.json."

    assert data["vocab_size"] == 16, f"Expected vocab_size to be 16, got {data['vocab_size']}."
    assert data["test_accuracy"] == 1.0, f"Expected test_accuracy to be 1.0, got {data['test_accuracy']}."