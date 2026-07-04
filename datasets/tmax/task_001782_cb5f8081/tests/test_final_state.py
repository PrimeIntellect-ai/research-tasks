# test_final_state.py

import os
import subprocess
import pytest

def test_cron_fixed():
    """Verify that the crontab for 'user' has been updated with required env vars."""
    try:
        output = subprocess.check_output(['crontab', '-l', '-u', 'user'], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to read crontab for user 'user'. Output: {e.output}")

    assert "LOG_DIR=/home/user/logs" in output, "crontab is missing LOG_DIR=/home/user/logs"
    assert "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" in output, "crontab is missing the required PATH"

def test_audio_filter_corpus():
    """Verify the Rust binary correctly classifies the clean and evil corpora."""
    binary_path = "/home/user/audio_filter/target/release/audio_filter"
    assert os.path.isfile(binary_path), f"Rust binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Rust binary at {binary_path} is not executable"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing at {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing at {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.wav')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.wav')]

    assert len(clean_files) > 0, "No clean files found to test."
    assert len(evil_files) > 0, "No evil files found to test."

    clean_failed = []
    for f in clean_files:
        result = subprocess.run([binary_path, f], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(f))

    evil_failed = []
    for f in evil_files:
        result = subprocess.run([binary_path, f], capture_output=True)
        if result.returncode != 1:
            evil_failed.append(os.path.basename(f))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected instead of accepted): {', '.join(clean_failed)}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed (accepted instead of rejected): {', '.join(evil_failed)}")

    if errors:
        pytest.fail(" | ".join(errors))