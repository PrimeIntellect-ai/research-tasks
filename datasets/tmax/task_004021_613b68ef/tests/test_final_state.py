# test_final_state.py
import os
import json
import subprocess
import pytest

def test_recovered_data():
    json_path = "/home/user/recovered_data.json"
    assert os.path.isfile(json_path), f"Recovered data file not found at {json_path}."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    expected = {
        "status": "recovered",
        "records": [
            {"id": 1, "fault": "OOM"},
            {"id": 2, "fault": "TIMEOUT"}
        ]
    }
    assert data == expected, f"Recovered data does not match expected output. Got: {data}"

def test_validator_adversarial_corpus():
    validator_path = "/home/user/validator"
    assert os.path.isfile(validator_path), f"Validator binary not found at {validator_path}."
    assert os.access(validator_path, os.X_OK), f"Validator binary at {validator_path} is not executable."

    evil_dir = "/app/corpus/evil"
    clean_dir = "/app/corpus/clean"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir)] if os.path.isdir(evil_dir) else []
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir)] if os.path.isdir(clean_dir) else []

    evil_bypassed = []
    for f in evil_files:
        result = subprocess.run([validator_path, f], capture_output=True)
        # Evil files should be rejected (exit code != 0)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(f))

    clean_modified = []
    for f in clean_files:
        result = subprocess.run([validator_path, f], capture_output=True)
        # Clean files should be accepted (exit code == 0)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(f))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))