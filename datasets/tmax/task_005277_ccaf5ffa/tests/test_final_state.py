# test_final_state.py
import os
import subprocess
import pytest

def test_alert_timestamps():
    output_file = "/home/user/alert_timestamps.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} is missing."

    with open(output_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # The expected timestamps based on the ground truth
    expected_timestamps = {
        "2024-03-15 23:00:01 JST",
        "2024-03-15 23:00:02 JST",
        "2024-03-15 23:00:05 JST",
        "2024-03-15 23:00:06 JST"
    }

    actual_timestamps = set(lines)

    missing = expected_timestamps - actual_timestamps
    unexpected = actual_timestamps - expected_timestamps

    assert not missing, f"Missing expected timestamps in output: {missing}"
    assert not unexpected, f"Found unexpected timestamps in output: {unexpected}"

def test_ssh_config_linter_adversarial_corpus():
    script_path = "/home/user/check_ssh_config.py"
    assert os.path.isfile(script_path), f"Linter script {script_path} is missing."

    evil_corpus_path = "/app/hidden_corpus/evil/"
    clean_corpus_path = "/app/hidden_corpus/clean/"

    assert os.path.isdir(evil_corpus_path), f"Evil corpus directory {evil_corpus_path} is missing."
    assert os.path.isdir(clean_corpus_path), f"Clean corpus directory {clean_corpus_path} is missing."

    evil_files = [os.path.join(evil_corpus_path, f) for f in os.listdir(evil_corpus_path) if os.path.isfile(os.path.join(evil_corpus_path, f))]
    clean_files = [os.path.join(clean_corpus_path, f) for f in os.listdir(clean_corpus_path) if os.path.isfile(os.path.join(clean_corpus_path, f))]

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus
    for evil_file in evil_files:
        result = subprocess.run(
            ["python3", script_path, evil_file],
            capture_output=True,
            text=True
        )
        stdout = result.stdout.strip()
        if result.returncode != 1 or stdout != "EVIL":
            evil_bypassed.append(os.path.basename(evil_file))

    # Test clean corpus
    for clean_file in clean_files:
        result = subprocess.run(
            ["python3", script_path, clean_file],
            capture_output=True,
            text=True
        )
        stdout = result.stdout.strip()
        if result.returncode != 0 or stdout != "CLEAN":
            clean_modified.append(os.path.basename(clean_file))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_modified)}")

    assert not error_messages, " | ".join(error_messages)