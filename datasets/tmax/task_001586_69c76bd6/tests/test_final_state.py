# test_final_state.py

import os
import glob
import json
import subprocess
import pytest

def test_extracted_payload_exists_and_valid():
    payload_path = "/app/extracted_payload.json"
    assert os.path.isfile(payload_path), f"Missing extracted payload: {payload_path}"

    with open(payload_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {payload_path} is not valid JSON.")

    assert isinstance(data, list), f"Expected {payload_path} to contain a JSON list."
    # We expect the list to contain numbers or strings representing numbers (e.g., denormalized floats)
    assert len(data) > 0, f"Extracted payload is empty."

def test_detector_clean_corpus():
    detector_path = "/app/detector.py"
    assert os.path.isfile(detector_path), f"Missing detector script: {detector_path}"

    clean_dir = "/app/corpus/clean"
    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run(["python3", detector_path, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files modified/rejected (expected exit code 0). Offending files: {', '.join(failed_files[:10])}")

def test_detector_evil_corpus():
    detector_path = "/app/detector.py"
    assert os.path.isfile(detector_path), f"Missing detector script: {detector_path}"

    evil_dir = "/app/corpus/evil"
    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run(["python3", detector_path, filepath], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed (expected exit code 1). Offending files: {', '.join(failed_files[:10])}")