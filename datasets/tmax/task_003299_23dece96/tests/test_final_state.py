# test_final_state.py
import os
import json
import pytest

def test_bio_sim_c_reduction():
    file_path = "/home/user/bio_sim.c"
    assert os.path.isfile(file_path), f"File {file_path} is missing."
    with open(file_path, "r") as f:
        content = f.read()
    assert "reduction" in content, "The bio_sim.c file does not use OpenMP 'reduction' as required to fix the non-deterministic reduction."

def test_sim_result_json():
    file_path = "/home/user/sim_result.json"
    assert os.path.isfile(file_path), f"File {file_path} is missing. The notebook might not have been executed successfully."

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("sim_result.json does not contain valid JSON.")

    assert "state" in data, "sim_result.json is missing 'state' key."
    assert "mass" in data, "sim_result.json is missing 'mass' key."

    assert abs(data['state'][0] - 0.1219512) < 1e-4, f"Expected state[0] to be ~0.1219512, got {data['state'][0]}"
    assert abs(data['mass'] - 3.12195) < 1e-4, f"Expected mass to be ~3.12195, got {data['mass']}"