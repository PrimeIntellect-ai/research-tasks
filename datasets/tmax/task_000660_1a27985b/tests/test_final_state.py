# test_final_state.py

import os
import json
import pytest

def test_benchmark_script_exists():
    path = "/home/user/benchmark.sh"
    assert os.path.isfile(path), f"Expected bash script at {path} is missing."

def test_train_script_exists():
    path = "/home/user/train.py"
    assert os.path.isfile(path), f"Expected python script at {path} is missing."

def test_report_json():
    path = "/home/user/report.json"
    assert os.path.isfile(path), f"Expected report file at {path} is missing."

    with open(path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    assert "faster_model" in report, f"Key 'faster_model' missing in {path}"
    assert report["faster_model"] == "model_alpha", (
        f"Expected 'faster_model' to be 'model_alpha', got '{report['faster_model']}'"
    )

    assert "test_accuracy" in report, f"Key 'test_accuracy' missing in {path}"

    accuracy = report["test_accuracy"]
    assert isinstance(accuracy, (int, float)), f"'test_accuracy' must be a number, got {type(accuracy)}"

    expected_accuracy = 0.4
    assert abs(accuracy - expected_accuracy) < 0.01, (
        f"Expected 'test_accuracy' to be close to {expected_accuracy}, got {accuracy}"
    )