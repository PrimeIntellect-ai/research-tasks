# test_final_state.py
import os
import json
import pytest

def test_tracked_artifacts_jsonl():
    jsonl_path = "/home/user/tracked_artifacts.jsonl"
    assert os.path.exists(jsonl_path), f"The file {jsonl_path} is missing."
    assert os.path.isfile(jsonl_path), f"{jsonl_path} is not a file."

    expected_valid_experiments = {
        "EXP_001": {"accuracy": 0.95, "epoch_count": 100, "status": "SUCCESS"},
        "EXP_005": {"accuracy": 0.80, "epoch_count": 10, "status": "FAILED"},
        "EXP_008": {"accuracy": 0.91, "epoch_count": 40, "status": "SUCCESS"},
    }

    parsed_experiments = {}
    with open(jsonl_path, "r") as f:
        for line_num, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                exp_id = obj.get("experiment_id")
                assert exp_id, f"Line {line_num + 1} is missing 'experiment_id'."
                parsed_experiments[exp_id] = {
                    "accuracy": obj.get("accuracy"),
                    "epoch_count": obj.get("epoch_count"),
                    "status": obj.get("status")
                }
            except json.JSONDecodeError:
                pytest.fail(f"Line {line_num + 1} in {jsonl_path} is not valid JSON.")

    assert len(parsed_experiments) == len(expected_valid_experiments), \
        f"Expected {len(expected_valid_experiments)} valid experiments, found {len(parsed_experiments)}."

    for exp_id, expected_data in expected_valid_experiments.items():
        assert exp_id in parsed_experiments, f"Expected experiment {exp_id} is missing from {jsonl_path}."
        actual_data = parsed_experiments[exp_id]
        assert abs(actual_data["accuracy"] - expected_data["accuracy"]) < 1e-6, \
            f"Accuracy for {exp_id} does not match expected value."
        assert actual_data["epoch_count"] == expected_data["epoch_count"], \
            f"Epoch count for {exp_id} does not match expected value."
        assert actual_data["status"] == expected_data["status"], \
            f"Status for {exp_id} does not match expected value."

def test_invalid_rows_log():
    log_path = "/home/user/invalid_rows.log"
    assert os.path.exists(log_path), f"The file {log_path} is missing."
    assert os.path.isfile(log_path), f"{log_path} is not a file."

    expected_invalid_indices = {1, 2, 3, 5, 6}
    actual_invalid_indices = set()

    with open(log_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                actual_invalid_indices.add(int(line))
            except ValueError:
                pytest.fail(f"Invalid non-integer value found in {log_path}: {line}")

    assert actual_invalid_indices == expected_invalid_indices, \
        f"Expected invalid rows {expected_invalid_indices}, but got {actual_invalid_indices}."