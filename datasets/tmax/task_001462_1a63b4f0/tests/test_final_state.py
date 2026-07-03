# test_final_state.py

import os
import subprocess
import pytest
import glob

def test_plot_artifact_exists():
    """Verify that the plotting script successfully generated the artifact."""
    artifact_path = "/home/user/artifact_plot.png"
    assert os.path.isfile(artifact_path), f"Plot artifact is missing at {artifact_path}. Did the plotting script run successfully?"
    assert os.path.getsize(artifact_path) > 0, f"Plot artifact at {artifact_path} is empty."

def test_filter_logs_script_exists():
    """Verify that the log filtering script exists."""
    script_path = "/home/user/filter_logs.py"
    assert os.path.isfile(script_path), f"Filter script is missing at {script_path}."

def test_adversarial_corpus_filtering():
    """Verify that the log filter correctly accepts clean logs and rejects evil logs."""
    script_path = "/home/user/filter_logs.py"
    assert os.path.isfile(script_path), f"Cannot test filtering: {script_path} does not exist."

    clean_dir = "/app/logs/clean"
    evil_dir = "/app/logs/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))

    assert len(clean_files) > 0, "No clean log files found to test."
    assert len(evil_files) > 0, "No evil log files found to test."

    clean_failures = []
    for clean_file in clean_files:
        result = subprocess.run(["python3", script_path, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(clean_file))

    evil_failures = []
    for evil_file in evil_files:
        result = subprocess.run(["python3", script_path, evil_file], capture_output=True)
        if result.returncode == 0:
            evil_failures.append(os.path.basename(evil_file))

    error_messages = []
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failures)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))