# test_final_state.py
import os
import json
import pytest

def test_results_json_exists():
    path = "/home/user/results.json"
    assert os.path.isfile(path), f"Results file not found at {path}"

def test_results_json_content():
    path = "/home/user/results.json"
    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    required_keys = ["total_simulated_energy", "ks_stat", "p_value"]
    for key in required_keys:
        assert key in data, f"Missing key '{key}' in {path}"

    # Expected values derived from the deterministic numpy lognormal generation
    expected_energy = 3089450.418047
    expected_ks = 0.012540
    expected_p = 0.000000

    assert abs(data["total_simulated_energy"] - expected_energy) < 1e-5, \
        f"Incorrect total_simulated_energy: expected {expected_energy}, got {data['total_simulated_energy']}"

    assert abs(data["ks_stat"] - expected_ks) < 1e-5, \
        f"Incorrect ks_stat: expected {expected_ks}, got {data['ks_stat']}"

    assert abs(data["p_value"] - expected_p) < 1e-5, \
        f"Incorrect p_value: expected {expected_p}, got {data['p_value']}"

def test_analyze_script_exists():
    path = "/home/user/analyze.py"
    assert os.path.isfile(path), f"Analysis script not found at {path}"

def test_spectro_mc_fixed():
    path = "/home/user/sim/spectro_mc.py"
    assert os.path.isfile(path), f"Simulation script not found at {path}"

    with open(path, "r") as f:
        content = f.read()

    assert "imap_unordered" not in content, \
        "The simulation script still contains 'imap_unordered', which causes non-deterministic ordering."
    assert "math.fsum" in content, \
        "The simulation script does not use 'math.fsum' to compute the total energy deterministically."