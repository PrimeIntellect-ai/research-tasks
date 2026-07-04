# test_final_state.py
import os
import json
import pytest

def test_catalog_output_exists():
    output_path = "/home/user/catalog_output.json"
    assert os.path.exists(output_path), f"Output file {output_path} does not exist. Did you run the script?"
    assert os.path.isfile(output_path), f"{output_path} is not a file."

def test_catalog_output_content():
    output_path = "/home/user/catalog_output.json"

    try:
        with open(output_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to load JSON from {output_path}: {e}")

    assert isinstance(data, list), "The output JSON should be a list of products."
    assert len(data) == 2, f"Expected exactly 2 items in the output, but found {len(data)}."

    # Check Widget A
    widget_a = next((item for item in data if item.get("id") == 1), None)
    assert widget_a is not None, "Widget A (id=1) is missing from the output."
    assert widget_a.get("meta") == {"weight": 10, "color": "red"}, "Widget A has incorrect meta data."

    # Check Widget B
    widget_b = next((item for item in data if item.get("id") == 2), None)
    assert widget_b is not None, "Widget B (id=2) is missing from the output."
    assert widget_b.get("meta") == {"weight": 15, "color": "blue"}, "Widget B has incorrect meta data. Did you parse the anomalous serialization correctly?"

    # Check Widget C is NOT present
    widget_c = next((item for item in data if item.get("id") == 3), None)
    assert widget_c is None, "Widget C (id=3, deleted) was found in output. Query result filtering failed."