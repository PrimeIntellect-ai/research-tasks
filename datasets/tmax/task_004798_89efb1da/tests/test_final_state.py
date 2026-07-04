# test_final_state.py
import os
import json

def test_profiler_go_exists():
    file_path = "/home/user/profiler.go"
    assert os.path.isfile(file_path), f"Expected Go program {file_path} does not exist."

def test_best_model_json_exists_and_correct():
    file_path = "/home/user/best_model.json"
    assert os.path.isfile(file_path), f"Expected output file {file_path} does not exist."

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {file_path} does not contain valid JSON."

    assert "hypothesis" in data, f"Key 'hypothesis' is missing from {file_path}."
    assert data["hypothesis"] == "B", f"Expected hypothesis 'B', but got '{data['hypothesis']}'."