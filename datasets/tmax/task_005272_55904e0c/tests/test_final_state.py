# test_final_state.py

import os
import json
import pytest

def test_report_exists_and_valid():
    report_path = "/home/user/model_eval/report.json"
    assert os.path.isfile(report_path), f"Expected report file at {report_path} does not exist."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Could not parse {report_path} as JSON: {e}")

    assert "best_k" in data, "JSON is missing 'best_k' key."
    assert "cv_accuracy" in data, "JSON is missing 'cv_accuracy' key."
    assert "benchmark_time_us" in data, "JSON is missing 'benchmark_time_us' key."

    # Check best_k
    assert float(data["best_k"]) == 5.0, f"Expected best_k to be 5.0, got {data['best_k']}."

    # Check cv_accuracy
    cv_acc = float(data["cv_accuracy"])
    assert 0.83 <= cv_acc <= 0.84, f"Expected cv_accuracy to be between 0.83 and 0.84, got {cv_acc}."

    # Check benchmark_time_us
    bench_time = data["benchmark_time_us"]
    assert isinstance(bench_time, (int, float)), "benchmark_time_us must be a number."
    assert bench_time > 0, f"Expected benchmark_time_us to be > 0, got {bench_time}."