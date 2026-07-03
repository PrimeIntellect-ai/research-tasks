# test_final_state.py

import os
import json
import pytest

def get_expected_values():
    valid_temps = []
    with open('/home/user/sensor_data.csv', 'r') as f:
        next(f) # skip header
        for line in f:
            parts = line.strip('\n').split(',')
            if len(parts) >= 3:
                temp_str = parts[2]
                if temp_str != "" and temp_str != "NA":
                    valid_temps.append(float(temp_str))

    N = len(valid_temps)
    original_mean = sum(valid_temps) / N

    seed = 42
    def my_rand():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) & 0x7fffffff
        return seed

    bootstrap_means = []
    for b in range(10000):
        b_sum = 0.0
        for _ in range(N):
            idx = my_rand() % N
            b_sum += valid_temps[idx]
        bootstrap_means.append(b_sum / N)

    bootstrap_means.sort()
    ci_lower = bootstrap_means[250]
    ci_upper = bootstrap_means[9750]

    return original_mean, ci_lower, ci_upper

def test_c_source_exists():
    assert os.path.exists('/home/user/bootstrap_ci.c'), "Source file /home/user/bootstrap_ci.c is missing."

def test_executable_exists():
    assert os.path.exists('/home/user/bootstrap_ci'), "Executable /home/user/bootstrap_ci is missing."
    assert os.access('/home/user/bootstrap_ci', os.X_OK), "File /home/user/bootstrap_ci is not executable."

def test_result_json():
    result_path = '/home/user/result.json'
    assert os.path.exists(result_path), f"{result_path} is missing."

    with open(result_path, 'r') as f:
        try:
            actual_json = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{result_path} does not contain valid JSON.")

    assert "original_mean" in actual_json, "Missing 'original_mean' in result.json"
    assert "ci_lower" in actual_json, "Missing 'ci_lower' in result.json"
    assert "ci_upper" in actual_json, "Missing 'ci_upper' in result.json"

    orig, lower, upper = get_expected_values()

    expected_orig = round(orig, 2)
    expected_lower = round(lower, 2)
    expected_upper = round(upper, 2)

    assert abs(actual_json["original_mean"] - expected_orig) < 0.01, f"Expected original_mean around {expected_orig}, got {actual_json['original_mean']}"
    assert abs(actual_json["ci_lower"] - expected_lower) < 0.01, f"Expected ci_lower around {expected_lower}, got {actual_json['ci_lower']}"
    assert abs(actual_json["ci_upper"] - expected_upper) < 0.01, f"Expected ci_upper around {expected_upper}, got {actual_json['ci_upper']}"