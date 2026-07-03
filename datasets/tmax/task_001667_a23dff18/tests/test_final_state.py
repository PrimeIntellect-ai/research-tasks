# test_final_state.py

import os
import json
import subprocess
import pytest

def test_baseline_stats():
    stats_path = "/home/user/baseline_stats.json"
    assert os.path.isfile(stats_path), f"Missing {stats_path}"

    with open(stats_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {stats_path} is not valid JSON.")

    assert "ci_lower" in data, "Missing 'ci_lower' in baseline_stats.json"
    assert "ci_upper" in data, "Missing 'ci_upper' in baseline_stats.json"
    assert isinstance(data["ci_lower"], (float, int)), "'ci_lower' must be a number"
    assert isinstance(data["ci_upper"], (float, int)), "'ci_upper' must be a number"
    assert data["ci_lower"] <= data["ci_upper"], "'ci_lower' must be <= 'ci_upper'"

def test_filter_script_exists():
    script_path = "/home/user/filter.py"
    assert os.path.isfile(script_path), f"Missing filter script: {script_path}"

def test_filter_behavior():
    script_path = "/home/user/filter.py"
    clean_dir = "/app/test/clean"
    evil_dir = "/app/test/evil"

    assert os.path.isdir(clean_dir), f"Missing clean directory: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Missing evil directory: {evil_dir}"

    clean_files = sorted([os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.wav')])
    evil_files = sorted([os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.wav')])

    failed_clean = []
    failed_evil = []

    for fpath in clean_files:
        res = subprocess.run(["python3", script_path, fpath], capture_output=True)
        if res.returncode != 0:
            failed_clean.append(os.path.basename(fpath))

    for fpath in evil_files:
        res = subprocess.run(["python3", script_path, fpath], capture_output=True)
        if res.returncode != 1:
            failed_evil.append(os.path.basename(fpath))

    errors = []
    if failed_evil:
        errors.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil)}")
    if failed_clean:
        errors.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean)}")

    if errors:
        pytest.fail(" | ".join(errors))