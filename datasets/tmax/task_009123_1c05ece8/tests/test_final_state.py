# test_final_state.py
import os
import json
import pytest

def test_experiment_log_exists_and_correct():
    log_path = "/home/user/experiment_log.json"
    expected_path = "/home/user/.expected_log.json"

    assert os.path.isfile(log_path), f"File {log_path} is missing. The C program did not output the experiment log."
    assert os.path.isfile(expected_path), f"Ground truth file {expected_path} is missing."

    with open(log_path, 'r') as f:
        try:
            student_log = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {log_path} is not a valid JSON file.")

    with open(expected_path, 'r') as f:
        expected_log = json.load(f)

    assert "best_epsilon" in student_log, "Key 'best_epsilon' is missing from the experiment log."
    assert "best_accuracy" in student_log, "Key 'best_accuracy' is missing from the experiment log."

    student_eps = float(student_log["best_epsilon"])
    student_acc = float(student_log["best_accuracy"])

    expected_eps = float(expected_log["best_epsilon"])
    expected_acc = float(expected_log["best_accuracy"])

    assert f"{student_eps:.2f}" == f"{expected_eps:.2f}", f"Expected best_epsilon {expected_eps:.2f}, but got {student_eps:.2f}."
    assert f"{student_acc:.2f}" == f"{expected_acc:.2f}", f"Expected best_accuracy {expected_acc:.2f}, but got {student_acc:.2f}."