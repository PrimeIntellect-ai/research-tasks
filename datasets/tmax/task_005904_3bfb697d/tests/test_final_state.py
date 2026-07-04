# test_final_state.py

import os
import json
import pytest

def test_posterior_mean_file_exists():
    file_path = "/home/user/posterior_mean.json"
    assert os.path.exists(file_path), f"The required output file {file_path} does not exist."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_posterior_mean_content():
    file_path = "/home/user/posterior_mean.json"

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to read {file_path} as a JSON file. Error: {e}")

    assert "gamma" in data, "Key 'gamma' is missing from the JSON file."
    assert "omega" in data, "Key 'omega' is missing from the JSON file."

    gamma = data["gamma"]
    omega = data["omega"]

    assert isinstance(gamma, (int, float)), f"Expected 'gamma' to be a number, got {type(gamma)}"
    assert isinstance(omega, (int, float)), f"Expected 'omega' to be a number, got {type(omega)}"

    assert 0.130 <= gamma <= 0.170, f"Gamma value {gamma} is out of the expected bounds [0.130, 0.170]"
    assert 3.120 <= omega <= 3.160, f"Omega value {omega} is out of the expected bounds [3.120, 3.160]"

def test_posterior_mean_rounding():
    file_path = "/home/user/posterior_mean.json"

    with open(file_path, 'r') as f:
        content = f.read()
        data = json.loads(content)

    gamma_str = str(data["gamma"])
    omega_str = str(data["omega"])

    if "." in gamma_str:
        assert len(gamma_str.split(".")[1]) <= 3, f"Gamma value {data['gamma']} is not rounded to 3 decimal places."
    if "." in omega_str:
        assert len(omega_str.split(".")[1]) <= 3, f"Omega value {data['omega']} is not rounded to 3 decimal places."