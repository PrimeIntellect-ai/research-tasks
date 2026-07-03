# test_final_state.py

import os
import subprocess
import pytest

def test_jq_built_successfully():
    jq_path = "/app/jq-1.6/jq"
    assert os.path.isfile(jq_path), f"jq binary not found at {jq_path}. Did you fix the Makefile and run make?"
    assert os.access(jq_path, os.X_OK), f"jq binary at {jq_path} is not executable."

    # Test execution to ensure it was built correctly
    result = subprocess.run([jq_path, "--version"], capture_output=True, text=True)
    assert result.returncode == 0, f"jq binary failed to execute. stderr: {result.stderr}"

def test_telemetry_filter_adversarial_corpus():
    script_path = "/home/user/telemetry_filter.py"
    assert os.path.isfile(script_path), f"Telemetry filter script not found at {script_path}"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.json')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.json')]

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failed = []
    for cf in clean_files:
        with open(cf, 'r') as f:
            result = subprocess.run(["python3", script_path], stdin=f, capture_output=True)
            if result.returncode != 0:
                clean_failed.append(os.path.basename(cf))

    evil_failed = []
    for ef in evil_files:
        with open(ef, 'r') as f:
            result = subprocess.run(["python3", script_path], stdin=f, capture_output=True)
            if result.returncode != 1:
                evil_failed.append(os.path.basename(ef))

    error_messages = []
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        error_messages.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")

    assert not error_messages, " | ".join(error_messages)