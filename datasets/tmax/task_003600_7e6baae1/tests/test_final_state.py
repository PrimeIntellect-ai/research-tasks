# test_final_state.py

import os
import json
import subprocess
import pytest

def test_summary_json():
    summary_path = "/home/user/summary.json"
    assert os.path.exists(summary_path), f"Summary file missing at {summary_path}"

    with open(summary_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {summary_path} is not valid JSON")

    assert isinstance(data, list), "Summary JSON should be a list of objects"
    assert len(data) == 3, f"Expected 3 segments, found {len(data)}"

    durations = sorted([float(item.get("duration", 0)) for item in data], reverse=True)

    # Expected approximate durations: 18.0, 17.0, 15.0
    expected = [18.0, 17.0, 15.0]
    for i, (actual, exp) in enumerate(zip(durations, expected)):
        assert abs(actual - exp) < 2.0, f"Segment {i+1} duration {actual} is not close to expected {exp}"

def test_adversarial_corpus():
    binary_path = "/home/user/etl_tool/target/debug/etl_tool"
    assert os.path.exists(binary_path), f"Rust binary missing at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Rust binary at {binary_path} is not executable"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.json')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.json')]

    clean_failed = []
    evil_failed = []

    for cf in clean_files:
        result = subprocess.run([binary_path, "sanitize", cf], capture_output=True, text=True)
        if "ACCEPT" not in result.stdout:
            clean_failed.append(os.path.basename(cf))

    for ef in evil_files:
        result = subprocess.run([binary_path, "sanitize", ef], capture_output=True, text=True)
        if "REJECT" not in result.stdout:
            evil_failed.append(os.path.basename(ef))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed[:5])}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed[:5])}")

    if errors:
        pytest.fail(" | ".join(errors))