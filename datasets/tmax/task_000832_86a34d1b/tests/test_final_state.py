# test_final_state.py

import os
import json
import stat
import pytest

def test_simulator_executable_exists():
    path = "/home/user/simulator"
    assert os.path.isfile(path), f"Executable {path} is missing."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."

def test_observations_csv_exists():
    path = "/home/user/observations.csv"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert "seqA,42.1,44.5,43.2,41.8,45.0" in content, f"File {path} does not contain the expected CSV data for seqA."
    assert "seqB,25.4,26.1,24.8,25.9,27.0" in content, f"File {path} does not contain the expected CSV data for seqB."
    assert "seqC,50.1,48.5,49.2,51.0,49.8" in content, f"File {path} does not contain the expected CSV data for seqC."

def test_probabilities_json_exists_and_correct():
    path = "/home/user/probabilities.json"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} does not contain valid JSON.")

    expected_data = {
        "seqA": 0.1085,
        "seqB": 0.0,
        "seqC": 1.0
    }

    for seq, expected_prob in expected_data.items():
        assert seq in data, f"Sequence {seq} is missing from the JSON output."
        assert isinstance(data[seq], (int, float)), f"Value for {seq} is not a number."
        assert round(data[seq], 4) == expected_prob, f"Probability for {seq} is incorrect. Expected {expected_prob}, got {data[seq]}."