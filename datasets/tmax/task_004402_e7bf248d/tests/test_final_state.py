# test_final_state.py

import os
import subprocess
import re
import pytest

def test_anomaly_seconds():
    path = "/home/user/anomaly_seconds.txt"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.splitlines() if line.strip()]
    assert len(lines) == 2, f"Expected exactly 2 lines in {path}, found {len(lines)}."

    seconds = set()
    for line in lines:
        try:
            seconds.add(int(line))
        except ValueError:
            pytest.fail(f"Invalid integer found in {path}: {line}")

    assert seconds == {3, 7}, f"Expected anomaly seconds {{3, 7}}, but got {seconds}."

def test_sanitizer_executable_exists():
    path = "/home/user/bin/sanitizer"
    assert os.path.isfile(path), f"Sanitizer executable {path} is missing."
    assert os.access(path, os.X_OK), f"Sanitizer {path} is not executable."

def test_sanitizer_adversarial_corpus():
    sanitizer_path = "/home/user/bin/sanitizer"
    assert os.path.isfile(sanitizer_path) and os.access(sanitizer_path, os.X_OK), "Sanitizer executable not found or not executable"

    evil_dir = "/app/corpora/evil/"
    clean_dir = "/app/corpora/clean/"

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    evil_bypassed = []
    clean_modified = []

    for f in evil_files:
        path = os.path.join(evil_dir, f)
        with open(path, 'rb') as fp:
            content = fp.read()
        proc = subprocess.run([sanitizer_path], input=content, capture_output=True)
        output = proc.stdout.replace(b'\n', b'').replace(b'\r', b'')
        if output != b'':
            evil_bypassed.append(f)

    for f in clean_files:
        path = os.path.join(clean_dir, f)
        with open(path, 'rb') as fp:
            content = fp.read()
        proc = subprocess.run([sanitizer_path], input=content, capture_output=True)

        # Normalize line endings for comparison
        expected = content.replace(b'\r\n', b'\n').strip()
        actual = proc.stdout.replace(b'\r\n', b'\n').strip()

        if expected != actual:
            clean_modified.append(f)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not error_msgs, "; ".join(error_msgs)

def test_sanitized_anomalies():
    path = "/home/user/sanitized_anomalies.txt"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.splitlines() if line.strip()]
    expected_lines = ["Anomaly trace 1", "Anomaly trace 2"]

    assert lines == expected_lines, f"Expected lines {expected_lines} in {path}, but got {lines}."

def test_cron_schedule():
    path = "/home/user/pipeline.cron"
    assert os.path.isfile(path), f"Cron schedule file {path} is missing."

    with open(path, "r") as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith('#')]
    assert len(lines) > 0, f"No active cron jobs found in {path}."

    valid_cron_found = False
    for line in lines:
        if "/home/user/run_pipeline.sh" in line:
            # Check for every 15 minutes pattern
            if line.startswith("*/15 * * * *") or line.startswith("0,15,30,45 * * * *"):
                valid_cron_found = True
                break

    assert valid_cron_found, f"Could not find a valid cron schedule for every 15 minutes running /home/user/run_pipeline.sh in {path}. Found: {content}"