# test_final_state.py
import os
import json
import re
import pytest

def test_analyze_go_exists_and_uses_concurrency():
    """Check that analyze.go exists and uses goroutines and WaitGroup."""
    go_file = "/home/user/analyze.go"
    assert os.path.exists(go_file), f"The file {go_file} does not exist."
    assert os.path.isfile(go_file), f"{go_file} is not a file."

    with open(go_file, 'r', encoding='utf-8') as f:
        content = f.read()

    assert re.search(r'\bgo\s+', content), f"No goroutines ('go ' keyword) found in {go_file}."
    assert "sync.WaitGroup" in content or "WaitGroup" in content, f"sync.WaitGroup not found in {go_file}."

def test_peak_ci_json_exists_and_valid():
    """Check that peak_ci.json exists, is valid JSON, and has correct bounds."""
    json_file = "/home/user/peak_ci.json"
    assert os.path.exists(json_file), f"The file {json_file} does not exist."
    assert os.path.isfile(json_file), f"{json_file} is not a file."

    with open(json_file, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {json_file} as JSON: {e}")

    required_keys = {"mean_com", "ci_lower", "ci_upper"}
    assert required_keys.issubset(data.keys()), f"{json_file} is missing one or more required keys: {required_keys - data.keys()}"

    mean_com = data["mean_com"]
    ci_lower = data["ci_lower"]
    ci_upper = data["ci_upper"]

    assert isinstance(mean_com, (int, float)), "mean_com must be a number"
    assert isinstance(ci_lower, (int, float)), "ci_lower must be a number"
    assert isinstance(ci_upper, (int, float)), "ci_upper must be a number"

    assert 451.8 <= mean_com <= 452.2, f"mean_com {mean_com} is out of expected bounds (451.8 - 452.2)"
    assert 451.4 <= ci_lower <= 451.8, f"ci_lower {ci_lower} is out of expected bounds (451.4 - 451.8)"
    assert 452.1 <= ci_upper <= 452.5, f"ci_upper {ci_upper} is out of expected bounds (452.1 - 452.5)"