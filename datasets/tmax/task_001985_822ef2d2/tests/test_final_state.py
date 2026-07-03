# test_final_state.py

import os
import json
import subprocess
import pytest

def test_log_sanitizer_adversarial_corpus():
    script_path = "/home/user/log_sanitizer.py"
    assert os.path.exists(script_path), f"Missing script: {script_path}"

    clean_dir = "/app/corpora/clean/"
    evil_dir = "/app/corpora/evil/"

    assert os.path.exists(clean_dir), f"Missing directory: {clean_dir}"
    assert os.path.exists(evil_dir), f"Missing directory: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith(".csv")]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith(".csv")]

    assert len(clean_files) > 0, "No clean corpus files found to test."
    assert len(evil_files) > 0, "No evil corpus files found to test."

    clean_failed = []
    for cf in clean_files:
        res = subprocess.run(["python3", script_path, cf], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    evil_failed = []
    for ef in evil_files:
        res = subprocess.run(["python3", script_path, ef], capture_output=True)
        if res.returncode == 0:
            evil_failed.append(os.path.basename(ef))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {clean_failed}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {evil_failed}")

    if errors:
        pytest.fail(" | ".join(errors))

def test_visual_telemetry_exists():
    path = "/home/user/visual_telemetry.csv"
    assert os.path.exists(path), f"Missing visual telemetry output: {path}"
    assert os.path.isfile(path), f"Expected {path} to be a file"

def test_strata_summary_exists_and_format():
    path = "/home/user/strata_summary.json"
    assert os.path.exists(path), f"Missing final aggregation output: {path}"

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON")

    assert isinstance(data, dict), "Root JSON object must be a dictionary"

    for key, value in data.items():
        assert isinstance(key, str), f"Keys must be strings, got {type(key)}"
        assert key.isdigit(), f"Keys must be string representation of integers (e.g. '0', '5'), got {key}"
        assert isinstance(value, dict), f"Value for key {key} must be a dictionary"

        expected_keys = {"mean_luminance", "mean_sensor", "count_luminance", "count_sensor"}
        missing_keys = expected_keys - set(value.keys())
        assert not missing_keys, f"Missing keys {missing_keys} in stratum {key}"

        for k in expected_keys:
            assert isinstance(value[k], (int, float)), f"Expected numeric value for {k} in stratum {key}"