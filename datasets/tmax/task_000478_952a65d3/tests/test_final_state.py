# test_final_state.py

import os
import json
import pytest

SCRIPT_PATH = "/home/user/analyze_network.py"
OUTPUT_PATH = "/home/user/shortest_path.json"

def test_script_exists():
    """Check that the student's script exists."""
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"

def test_output_json_exists():
    """Check that the output JSON file exists."""
    assert os.path.exists(OUTPUT_PATH), f"Output JSON not found at {OUTPUT_PATH}. Did you run the script?"
    assert os.path.isfile(OUTPUT_PATH), f"{OUTPUT_PATH} is not a file"

def test_output_json_content():
    """Check that the output JSON file contains the correct shortest path result."""
    with open(OUTPUT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_PATH} does not contain valid JSON.")

    assert "path" in data, "JSON output is missing the 'path' key."
    assert "total_weight" in data, "JSON output is missing the 'total_weight' key."

    expected_path = ["Protein_A", "Chemical_C", "Protein_D", "Disease_Z"]
    expected_weight = 18.0

    assert data["path"] == expected_path, f"Expected path {expected_path}, but got {data['path']}."
    assert data["total_weight"] == expected_weight, f"Expected total_weight {expected_weight}, but got {data['total_weight']}."