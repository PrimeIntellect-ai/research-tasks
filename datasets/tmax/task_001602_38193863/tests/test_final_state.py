# test_final_state.py

import os
import subprocess
import pytest

def test_filter_executable_exists():
    assert os.path.isfile("/app/bin/filter"), "/app/bin/filter does not exist. Did you compile the C program?"
    assert os.access("/app/bin/filter", os.X_OK), "/app/bin/filter is not executable."

def test_adversarial_corpus_filter():
    filter_bin = "/app/bin/filter"
    evil_dir = "/app/eval_corpus/evil"
    clean_dir = "/app/eval_corpus/clean"

    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} missing"
    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} missing"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.csv')]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.csv')]

    assert len(evil_files) > 0, "No evil corpus files found to test."
    assert len(clean_files) > 0, "No clean corpus files found to test."

    evil_bypassed = []
    for filepath in evil_files:
        result = subprocess.run([filter_bin, filepath], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(filepath))

    clean_modified = []
    for filepath in clean_files:
        result = subprocess.run([filter_bin, filepath], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(filepath))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_modified)}")

    assert not errors, "Adversarial filter failed:\n" + "\n".join(errors)

def test_flask_env_configuration():
    env_path = "/app/config/flask.env"
    assert os.path.isfile(env_path), f"{env_path} is missing."

    with open(env_path, "r") as f:
        content = f.read()

    assert "redis://localhost:6379" in content, "REDIS_URL in flask.env was not updated to port 6379."
    assert "redis://localhost:6380" not in content, "Old REDIS_URL port 6380 is still present in flask.env."

def test_start_sh_configuration():
    start_sh_path = "/app/start.sh"
    assert os.path.isfile(start_sh_path), f"{start_sh_path} is missing."

    with open(start_sh_path, "r") as f:
        content = f.read()

    assert "redis-server" in content, "redis-server is not being launched in start.sh."