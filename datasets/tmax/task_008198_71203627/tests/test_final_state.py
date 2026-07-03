# test_final_state.py
import os
import json
import math

def test_raw_logs_transferred():
    raw_logs_dir = "/home/user/analysis/raw_logs"
    for i in range(1, 4):
        log_file = os.path.join(raw_logs_dir, f"server_{i}.log")
        assert os.path.isfile(log_file), f"Expected copied log file is missing: {log_file}"
        assert os.path.getsize(log_file) > 0, f"Copied log file is empty: {log_file}"

def test_results_json():
    results_file = "/home/user/analysis/results.json"
    assert os.path.isfile(results_file), f"Results file is missing: {results_file}"

    with open(results_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"Results file is not valid JSON: {results_file}"

    assert "closest_pair" in data, "Key 'closest_pair' missing from results.json"
    assert "distance" in data, "Key 'distance' missing from results.json"

    closest_pair = data["closest_pair"]
    assert isinstance(closest_pair, list), "'closest_pair' should be a list"
    assert len(closest_pair) == 2, "'closest_pair' should contain exactly two elements"

    # Sort closest_pair to handle any order, though task constraints say it must be sorted
    assert closest_pair == sorted(closest_pair), "'closest_pair' must be sorted alphabetically"
    assert closest_pair == ["server_1", "server_3"], f"Expected closest pair ['server_1', 'server_3'], got {closest_pair}"

    distance = data["distance"]
    assert isinstance(distance, (int, float)), "'distance' should be a number"

    expected_distance = round(math.sqrt(3), 2)
    assert distance == expected_distance, f"Expected distance {expected_distance}, got {distance}"