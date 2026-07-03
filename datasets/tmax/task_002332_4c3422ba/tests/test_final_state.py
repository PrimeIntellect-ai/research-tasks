# test_final_state.py
import os
import json

def test_executable_compiled():
    exe_path = "/home/user/filter_seqs"
    assert os.path.isfile(exe_path), f"Executable {exe_path} was not found. Did you compile the C program?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_filtered_output():
    out_path = "/home/user/filtered.txt"
    assert os.path.isfile(out_path), f"Filtered output file {out_path} was not found."

    with open(out_path, "r") as f:
        content = f.read().strip().split('\n')

    # Check that TARGET_SEQ is in the output and properly formatted
    target_found = False
    for line in content:
        if line.startswith("TARGET_SEQ,"):
            target_found = True
            seq = line.split(",")[1]
            assert len(seq) >= 30, "TARGET_SEQ length in filtered.txt is incorrect."
            break

    assert target_found, "TARGET_SEQ was not found in the filtered output."

def test_analyze_script_exists():
    script_path = "/home/user/analyze.py"
    assert os.path.isfile(script_path), f"Python script {script_path} was not found."

def test_spectral_results_json():
    json_path = "/home/user/spectral_results.json"
    assert os.path.isfile(json_path), f"JSON results file {json_path} was not found."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} is not valid JSON."

    assert "TARGET_SEQ" in data, "Key 'TARGET_SEQ' is missing from the JSON output."

    weights = data["TARGET_SEQ"]
    expected_keys = {"w_A", "w_C", "w_G", "w_T"}
    assert set(weights.keys()) == expected_keys, f"JSON weights keys must be exactly {expected_keys}."

    # Check bounds and sum
    w_sum = sum(weights.values())
    assert abs(w_sum - 1.0) < 1e-3, f"Weights must sum to 1.0, but got {w_sum}."

    for k, v in weights.items():
        assert 0.0 <= v <= 1.0, f"Weight {k} is out of bounds [0, 1]: {v}"

    # Based on the truth data for ATTATT..., w_A should be the maximum
    assert weights["w_A"] >= 0.99, f"Expected w_A to be near 1.0, got {weights['w_A']}."
    assert weights["w_C"] <= 0.01, f"Expected w_C to be near 0.0, got {weights['w_C']}."
    assert weights["w_G"] <= 0.01, f"Expected w_G to be near 0.0, got {weights['w_G']}."
    assert weights["w_T"] <= 0.01, f"Expected w_T to be near 0.0, got {weights['w_T']}."