# test_final_state.py

import os
import json
import pytest
import sys
import importlib.util

def test_final_diff_json():
    file_path = '/home/user/final_diff.json'
    assert os.path.isfile(file_path), f"The file {file_path} does not exist. Did you run main.py?"

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{file_path} is not valid JSON.")

    expected_data = [[1, 5.0], [8, 2.0], [15, 5.0], [20, 5.0]]
    assert data == expected_data, f"Expected {expected_data} in {file_path}, but got {data}"

def test_test_analyzer_has_mock():
    file_path = '/home/user/metrics_analyzer/test_analyzer.py'
    assert os.path.isfile(file_path), f"The file {file_path} does not exist."

    with open(file_path, 'r') as f:
        content = f.read()

    assert "patch" in content, "test_analyzer.py does not use unittest.mock.patch as required."
    assert "process_streams" in content, "test_analyzer.py does not test process_streams."

def test_merge_and_diff_logic():
    # Dynamically import analyzer.py to test the algorithm
    file_path = '/home/user/metrics_analyzer/analyzer.py'
    assert os.path.isfile(file_path), f"The file {file_path} does not exist."

    spec = importlib.util.spec_from_file_location("analyzer", file_path)
    analyzer = importlib.util.module_from_spec(spec)
    sys.modules["analyzer"] = analyzer
    spec.loader.exec_module(analyzer)

    assert hasattr(analyzer, 'merge_and_diff'), "merge_and_diff function missing in analyzer.py"

    # Test normal matching
    stream_a = [(10, 100.0), (20, 150.0), (30, 200.0)]
    stream_b = [(12, 105.0), (19, 140.0), (35, 210.0)]
    res = analyzer.merge_and_diff(stream_a, stream_b)
    assert res == [[10, 5.0], [20, 10.0]], f"merge_and_diff failed on basic mock data. Got {res}"

    # Test tie breaking logic:
    # "If there is still a tie (e.g., tb is 2 units before and another tb is 2 units after), 
    # choose the one with the smaller vb (metric_value)."
    stream_a_tie = [(10, 100.0)]
    stream_b_tie = [(8, 110.0), (12, 105.0)] # Both diff in time is 2. Values are 110 and 105.
    # Should pick (12, 105.0) because 105.0 < 110.0
    # Diff in values: abs(100.0 - 105.0) = 5.0
    res_tie = analyzer.merge_and_diff(stream_a_tie, stream_b_tie)
    assert res_tie == [[10, 5.0]], f"merge_and_diff failed tie-breaking logic. Got {res_tie}"

    # Test out of bounds (abs(ta - tb) < 5)
    stream_a_out = [(10, 100.0)]
    stream_b_out = [(15, 110.0)] # diff is 5, condition is < 5, so no match
    res_out = analyzer.merge_and_diff(stream_a_out, stream_b_out)
    assert res_out == [], f"merge_and_diff failed out of bounds logic (must be strictly < 5). Got {res_out}"