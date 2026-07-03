# test_final_state.py

import os
import json
import pytest

def test_anomaly_file_exists_and_correct():
    anomaly_path = "/home/user/anomaly.txt"
    assert os.path.exists(anomaly_path), f"File {anomaly_path} does not exist."
    assert os.path.isfile(anomaly_path), f"Path {anomaly_path} is not a file."

    with open(anomaly_path, "r") as f:
        content = f.read().strip()

    assert content == "RUN_742", f"Expected 'RUN_742' in {anomaly_path}, but got '{content}'."

def test_success_json_exists_and_correct():
    success_path = "/home/user/success.json"
    assert os.path.exists(success_path), f"File {success_path} does not exist. Did the script run successfully?"
    assert os.path.isfile(success_path), f"Path {success_path} is not a file."

    with open(success_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {success_path} does not contain valid JSON.")

    assert "diffusion_center" in data, "Key 'diffusion_center' missing in success.json."
    assert "equilibrium" in data, "Key 'equilibrium' missing in success.json."

    assert data["diffusion_center"] == 80.0, f"Expected diffusion_center to be 80.0, got {data['diffusion_center']}."
    assert data["equilibrium"] == 50.0, f"Expected equilibrium to be 50.0, got {data['equilibrium']}."