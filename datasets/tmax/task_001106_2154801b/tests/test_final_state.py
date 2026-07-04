# test_final_state.py
import os
import json

def test_result_json_exists():
    path = "/home/user/result.json"
    assert os.path.exists(path), f"File {path} is missing."
    assert os.path.isfile(path), f"Path {path} is not a file."

def test_result_json_content():
    path = "/home/user/result.json"
    assert os.path.exists(path), f"File {path} is missing."

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            assert False, f"Failed to parse JSON in {path}: {e}"

    assert "f_peak" in data, "Key 'f_peak' is missing in result.json."
    assert "A" in data, "Key 'A' is missing in result.json."
    assert "phi" in data, "Key 'phi' is missing in result.json."

    f_peak = data["f_peak"]
    A = data["A"]
    phi = data["phi"]

    assert isinstance(f_peak, int) or (isinstance(f_peak, float) and f_peak.is_integer()), f"Expected 'f_peak' to be an integer, got {type(f_peak)}."
    assert f_peak == 7, f"Expected 'f_peak' to be 7, got {f_peak}."

    assert isinstance(A, (int, float)), f"Expected 'A' to be a number, got {type(A)}."
    assert 3.10 <= A <= 3.35, f"Expected 'A' to be between 3.10 and 3.35, got {A}."

    assert isinstance(phi, (int, float)), f"Expected 'phi' to be a number, got {type(phi)}."
    assert 0.65 <= phi <= 0.90, f"Expected 'phi' to be between 0.65 and 0.90, got {phi}."