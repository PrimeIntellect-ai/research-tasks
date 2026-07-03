# test_final_state.py

import os
import json
import pytest

def test_go_file_exists():
    assert os.path.isfile("/home/user/organizer.go"), "The Go program /home/user/organizer.go is missing."

def test_recommendations_csv():
    file_path = "/home/user/recommendations.csv"
    assert os.path.isfile(file_path), f"The file {file_path} is missing."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) >= 3, "recommendations.csv does not have enough rows."

    header = lines[0]
    assert header == "test_id,sim_1,sim_2,sim_3", f"Incorrect header in recommendations.csv: {header}"

    q1_row = lines[1]
    q2_row = lines[2]

    assert q1_row == "q1,t2,t1,t5", f"Incorrect recommendations for q1: {q1_row}"
    assert q2_row == "q2,t3,t4,t2", f"Incorrect recommendations for q2: {q2_row}"

def test_experiment_log_jsonl():
    file_path = "/home/user/experiment_log.jsonl"
    assert os.path.isfile(file_path), f"The file {file_path} is missing."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) >= 1, "experiment_log.jsonl is empty."

    last_log = lines[-1]
    try:
        data = json.loads(last_log)
    except json.JSONDecodeError:
        pytest.fail("The last line of experiment_log.jsonl is not valid JSON.")

    assert "k" in data, "Key 'k' is missing in experiment_log.jsonl."
    assert data["k"] == 3, f"Expected k=3, got {data['k']}"

    assert "accuracy" in data, "Key 'accuracy' is missing in experiment_log.jsonl."
    assert float(data["accuracy"]) == 1.0, f"Expected accuracy=1.0, got {data['accuracy']}"

    assert "throughput_qps" in data, "Key 'throughput_qps' is missing in experiment_log.jsonl."
    assert isinstance(data["throughput_qps"], (int, float)), "throughput_qps must be a number."
    assert data["throughput_qps"] > 0, "throughput_qps must be greater than 0."