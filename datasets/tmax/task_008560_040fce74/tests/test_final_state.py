# test_final_state.py
import os
import json
import math

def test_source_file_exists():
    assert os.path.isfile('/home/user/etl_inference.cpp'), "Source file /home/user/etl_inference.cpp does not exist."

def test_executable_exists():
    exe_path = '/home/user/etl_inference'
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"Executable {exe_path} is not executable."

def test_experiment_log():
    log_path = '/home/user/experiment_log.json'
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "Log file is not valid JSON."

    assert data.get("language") == "C++", f"Expected language to be 'C++', got {data.get('language')}"
    assert data.get("batch_size") == 1000000, f"Expected batch_size to be 1000000, got {data.get('batch_size')}"

    inference_time = data.get("inference_time_sec")
    assert isinstance(inference_time, (int, float)), "inference_time_sec must be a number."
    assert inference_time > 0.0, f"inference_time_sec must be greater than 0.0, got {inference_time}"

    sum_scores = data.get("sum_scores")
    assert isinstance(sum_scores, (int, float)), "sum_scores must be a number."

    # Calculate expected sum
    expected_sum = 0.0
    for i in range(1000000):
        x = i * 0.001
        expected_sum += 3.5*(x**3) - 1.2*(x**2) + 0.8*x - 4.1

    # Check within 0.01%
    tolerance = abs(expected_sum) * 0.0001
    assert math.isclose(sum_scores, expected_sum, abs_tol=tolerance), \
        f"sum_scores {sum_scores} is not within 0.01% of expected {expected_sum}"