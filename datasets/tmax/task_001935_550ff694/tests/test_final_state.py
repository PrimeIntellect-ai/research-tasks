# test_final_state.py

import os
import subprocess
import pytest

def test_baseline_transcription():
    """Verify that the baseline audio was correctly transcribed to /home/user/baseline.txt."""
    baseline_path = "/home/user/baseline.txt"
    assert os.path.exists(baseline_path), f"File {baseline_path} does not exist."

    with open(baseline_path, "r") as f:
        content = f.read().strip().splitlines()

    # Clean up any extra whitespaces
    content = [line.strip() for line in content if line.strip()]

    expected = ["42.7", "-0.003", "812"]
    assert content == expected, f"Baseline transcription is incorrect. Expected {expected}, got {content}"

def test_trace_filter_exists():
    """Verify that the trace_filter binary was compiled."""
    filter_path = "/home/user/trace_filter"
    assert os.path.exists(filter_path), f"Compiled binary {filter_path} does not exist."
    assert os.access(filter_path, os.X_OK), f"File {filter_path} is not executable."

def test_adversarial_corpus():
    """Verify the trace_filter binary against the clean and evil corpora."""
    filter_path = "/home/user/trace_filter"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} is missing."
    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} is missing."

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.json')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.json')]

    assert len(clean_files) > 0, "No clean JSON files found to test."
    assert len(evil_files) > 0, "No evil JSON files found to test."

    clean_failed = []
    for f in clean_files:
        result = subprocess.run([filter_path, f], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(f))

    evil_failed = []
    for f in evil_files:
        result = subprocess.run([filter_path, f], capture_output=True)
        if result.returncode == 0:
            evil_failed.append(os.path.basename(f))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failed)}")

    if errors:
        pytest.fail("Adversarial corpus validation failed:\n" + "\n".join(errors))