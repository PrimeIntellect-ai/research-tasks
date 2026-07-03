# test_final_state.py

import os
import json
import pytest

def load_jsonl(path):
    with open(path, 'r') as f:
        return [json.loads(line.strip()) for line in f if line.strip()]

def test_analyze_script_exists_and_executable():
    path = "/home/user/analyze.sh"
    assert os.path.exists(path), f"Missing script: {path}"
    assert os.path.isfile(path), f"Not a file: {path}"
    assert os.access(path, os.X_OK), f"Script is not executable: {path}"

def test_decoded_payloads_exists():
    path = "/home/user/decoded_payloads.jsonl"
    assert os.path.exists(path), f"Missing output file: {path}"
    assert os.path.isfile(path), f"Not a file: {path}"

def test_decoded_payloads_accuracy():
    target_file = "/home/user/decoded_payloads.jsonl"
    reference_file = "/opt/verifier/reference.jsonl"

    assert os.path.exists(target_file), f"Missing output file: {target_file}"
    assert os.path.exists(reference_file), f"Missing reference file: {reference_file}"

    try:
        reference = load_jsonl(reference_file)
    except Exception as e:
        pytest.fail(f"Failed to load reference file: {e}")

    try:
        candidate = load_jsonl(target_file)
    except Exception as e:
        pytest.fail(f"Failed to load candidate file (is it valid JSONL?): {e}")

    assert len(reference) > 0, "Reference file is empty."

    matches = 0
    for ref in reference:
        if ref in candidate:
            matches += 1

    accuracy = matches / len(reference)
    threshold = 0.95
    assert accuracy >= threshold, f"Accuracy {accuracy:.4f} is below the threshold of {threshold:.4f}."