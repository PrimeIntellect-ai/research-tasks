# test_final_state.py

import os
import json
import math
import subprocess

def test_anomalies_json_exists_and_correct():
    output_path = "/home/user/output/anomalies.json"
    assert os.path.isfile(output_path), f"Expected output file {output_path} does not exist."

    with open(output_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {output_path} is not valid JSON."

    assert isinstance(results, list), f"Expected {output_path} to contain a JSON array."
    assert len(results) == 4, f"Expected 4 results in {output_path}, found {len(results)}."

    # Expected calculations based on the formula: Euclidean_Distance(p1, p2) * e^(-0.1 * time_delta)
    # event_1: p1=(0,0), p2=(3,4), dist=5, time=10 -> 5 * exp(-1) = 1.8394
    # event_2: p1=(1,1), p2=(7,9), dist=10, time=5 -> 10 * exp(-0.5) = 6.0653
    # event_3: p1=(5,5), p2=(5,5), dist=0, time=0 -> 0 * exp(0) = 0.0
    # event_4: p1=(10,10), p2=(20,10), dist=10, time=2 -> 10 * exp(-0.2) = 8.1873

    expected = {
        "event_1": 1.8394,
        "event_2": 6.0653,
        "event_3": 0.0,
        "event_4": 8.1873
    }

    actual = {item.get("event_id"): item.get("score") for item in results if isinstance(item, dict)}

    for event_id, expected_score in expected.items():
        assert event_id in actual, f"Missing {event_id} in {output_path}."
        actual_score = actual[event_id]
        assert isinstance(actual_score, (int, float)), f"Score for {event_id} is not a number."
        assert math.isclose(actual_score, expected_score, abs_tol=1e-4), \
            f"Score for {event_id} is incorrect. Expected ~{expected_score}, got {actual_score}."

def test_regression_script_exists_and_passes():
    script_path = "/home/user/system/test_regression.py"
    assert os.path.isfile(script_path), f"Regression test script {script_path} does not exist."

    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Regression test script failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_processor_script_runnable():
    processor_path = "/home/user/system/processor.py"
    assert os.path.isfile(processor_path), f"Processor script {processor_path} does not exist."

    # Ensure it can be imported or parsed without syntax errors
    result = subprocess.run(["python3", "-m", "py_compile", processor_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Processor script has syntax errors:\n{result.stderr}"