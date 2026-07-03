# test_final_state.py

import os
import json
import pytest

JSON_PATH = "/home/user/shortest_path.json"
CPP_PATH = "/home/user/optimizer.cpp"

def test_cpp_file_exists():
    assert os.path.exists(CPP_PATH), f"C++ source file missing at {CPP_PATH}"
    assert os.path.isfile(CPP_PATH), f"{CPP_PATH} is not a file"

def test_json_output_exists():
    assert os.path.exists(JSON_PATH), f"Output JSON file missing at {JSON_PATH}"
    assert os.path.isfile(JSON_PATH), f"{JSON_PATH} is not a file"

def test_json_output_content():
    with open(JSON_PATH, 'r') as f:
        content = f.read()

    expected_str = '{"path":["Extract","Clean","Aggregate","Load"],"total_latency":30}'

    # Check exact string match as per requirements
    assert content.strip() == expected_str, (
        f"JSON content mismatch.\nExpected exact string: {expected_str}\n"
        f"Found: {content}"
    )

    # Also check JSON validity just in case
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail("Output file does not contain valid JSON.")

    assert data.get("path") == ["Extract", "Clean", "Aggregate", "Load"], "Incorrect path in JSON."
    assert data.get("total_latency") == 30, "Incorrect total_latency in JSON."