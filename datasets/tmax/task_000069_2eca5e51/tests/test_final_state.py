# test_final_state.py

import os
import json
import glob
import subprocess
import pytest

def test_video_results():
    results_path = "/home/user/video_results.json"
    assert os.path.exists(results_path), f"Expected results file at {results_path} does not exist."

    with open(results_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} is not valid JSON.")

    assert "successes" in data, "Missing 'successes' key in JSON."
    assert "failures" in data, "Missing 'failures' key in JSON."

    # Ground truth values derived from the task setup
    expected_successes = 60
    expected_failures = 90

    assert data["successes"] == expected_successes, f"Expected {expected_successes} successes, got {data['successes']}."
    assert data["failures"] == expected_failures, f"Expected {expected_failures} failures, got {data['failures']}."

def test_artifact_filter_executable():
    executable = "/home/user/artifact_filter"
    assert os.path.exists(executable), f"Compiled binary {executable} does not exist."
    assert os.access(executable, os.X_OK), f"Binary {executable} is not executable."

def test_adversarial_corpus_filtering():
    executable = "/home/user/artifact_filter"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.exists(executable), f"Missing executable {executable}"

    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))

    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}."
    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}."

    failed_clean = []
    for f in clean_files:
        res = subprocess.run([executable, f], capture_output=True)
        if res.returncode != 0:
            failed_clean.append(os.path.basename(f))

    failed_evil = []
    for f in evil_files:
        res = subprocess.run([executable, f], capture_output=True)
        # Expected to fail (exit code 1 or non-zero)
        if res.returncode == 0:
            failed_evil.append(os.path.basename(f))

    error_msgs = []
    if failed_evil:
        error_msgs.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil)}")
    if failed_clean:
        error_msgs.append(f"{len(failed_clean)} of {len(clean_files)} clean modified: {', '.join(failed_clean)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))