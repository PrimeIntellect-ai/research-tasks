# test_final_state.py

import os
import pytest

def test_redact_script_exists_and_executable():
    script_path = "/home/user/redact.sh"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_redacted_events_log_exists():
    log_path = "/home/user/redacted_events.log"
    assert os.path.exists(log_path), f"The output log {log_path} does not exist."
    assert os.path.isfile(log_path), f"{log_path} is not a file."
    assert os.path.getsize(log_path) > 0, f"The output log {log_path} is empty."

def test_redaction_accuracy():
    expected_path = "/app/expected_events.log"
    actual_path = "/home/user/redacted_events.log"

    assert os.path.exists(expected_path), f"Expected events log missing: {expected_path}"
    assert os.path.exists(actual_path), f"Actual events log missing: {actual_path}"

    with open(expected_path, 'r') as f:
        expected_lines = f.read().splitlines()

    with open(actual_path, 'r') as f:
        actual_lines = f.read().splitlines()

    assert len(expected_lines) > 0, "Expected events log is empty."
    assert len(expected_lines) == len(actual_lines), (
        f"Line count mismatch. Expected {len(expected_lines)} lines, "
        f"but got {len(actual_lines)} lines in {actual_path}."
    )

    correct = sum(1 for e, a in zip(expected_lines, actual_lines) if e == a)
    accuracy = correct / len(expected_lines)

    threshold = 0.99
    assert accuracy >= threshold, (
        f"Redaction accuracy is too low. "
        f"Expected >= {threshold}, but got {accuracy:.4f} "
        f"({correct}/{len(expected_lines)} lines matched)."
    )