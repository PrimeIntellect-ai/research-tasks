# test_final_state.py

import os
import json
import pytest

def test_summary_json_exists():
    path = '/home/user/summary.json'
    assert os.path.isfile(path), f"File missing: {path}. The script should generate this file."

def test_summary_json_content():
    path = '/home/user/summary.json'
    assert os.path.isfile(path), f"File missing: {path}"

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON in {path}")

    assert isinstance(data, list), f"The root of {path} should be a JSON array."

    results = {}
    for i, item in enumerate(data):
        assert isinstance(item, dict), f"Item at index {i} is not a JSON object."

        keys = set(item.keys())
        assert keys == {"customer_name", "total_spent"}, f"Item at index {i} has incorrect keys: {keys}. Expected exactly 'customer_name' and 'total_spent'."

        name = item["customer_name"]
        spent = item["total_spent"]

        assert isinstance(name, str), f"customer_name must be a string, got {type(name)} for {name}"
        assert isinstance(spent, (int, float)), f"total_spent must be a number, got {type(spent)} for {name}"

        results[name] = float(spent)

    assert "Alice" in results, "Missing customer 'Alice' in the summary."
    assert "Bob" in results, "Missing customer 'Bob' in the summary."

    assert abs(results["Alice"] - 40.5) < 1e-5, f"Incorrect total_spent for Alice. Expected 40.5, got {results['Alice']}"
    assert abs(results["Bob"] - 150.0) < 1e-5, f"Incorrect total_spent for Bob. Expected 150.0, got {results['Bob']}"

    if "Charlie" in results:
        assert abs(results["Charlie"] - 0.0) < 1e-5, f"Incorrect total_spent for Charlie. Expected 0.0, got {results['Charlie']}"