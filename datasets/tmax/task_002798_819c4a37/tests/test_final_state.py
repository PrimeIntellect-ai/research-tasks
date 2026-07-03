# test_final_state.py
import json
import os
import pytest

def load_logs(filepath):
    if not os.path.isfile(filepath):
        return []
    with open(filepath, 'r') as f:
        return [json.loads(line) for line in f if line.strip()]

def test_pyproject_toml_fixed():
    path = "/app/pyjwt-2.8.0/pyproject.toml"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, 'r') as f:
        content = f.read()

    assert 'requires = ["flit_core >=3.2,<4.0"]' in content, "The syntax error in pyproject.toml was not fixed."

def test_log_files_created():
    valid_path = "/home/user/valid_requests.log"
    invalid_path = "/home/user/invalid_requests.log"

    assert os.path.isfile(valid_path), f"Output file {valid_path} is missing."
    assert os.path.isfile(invalid_path), f"Output file {invalid_path} is missing."

def test_accuracy_metric():
    valid_preds = load_logs('/home/user/valid_requests.log')
    invalid_preds = load_logs('/home/user/invalid_requests.log')
    valid_gt = load_logs('/app/truth_valid.log')
    invalid_gt = load_logs('/app/truth_invalid.log')

    total = len(valid_gt) + len(invalid_gt)
    assert total > 0, "Ground truth files are empty or missing."

    correct = 0

    # Check exact matches in valid requests
    for pred in valid_preds:
        if pred in valid_gt:
            correct += 1

    # Check exact matches in invalid requests (ensuring REDACTED_CWE312 is present)
    for pred in invalid_preds:
        if pred in invalid_gt:
            correct += 1

    accuracy = correct / total
    assert accuracy >= 0.99, f"Accuracy {accuracy:.4f} is below the threshold of 0.99."