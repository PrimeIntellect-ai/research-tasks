# test_final_state.py
import os
import json
import pytest

def test_reconstructed_log():
    log_path = "/home/user/reconstructed.log"
    assert os.path.exists(log_path), f"File {log_path} does not exist."
    assert os.path.isfile(log_path), f"{log_path} is not a file."

    with open(log_path, "r") as f:
        lines = f.readlines()

    assert len(lines) == 30000, f"Expected exactly 30000 lines in {log_path}, found {len(lines)}."

    # Verify chronological sorting
    previous_timestamp = -1
    for i, line in enumerate(lines):
        parts = line.split()
        assert len(parts) > 0, f"Line {i+1} is empty or malformed."
        try:
            timestamp = int(parts[0])
        except ValueError:
            pytest.fail(f"Line {i+1} does not start with a valid integer timestamp: {line.strip()}")

        assert timestamp >= previous_timestamp, f"Log is not sorted chronologically. Line {i+1} timestamp {timestamp} is earlier than previous {previous_timestamp}."
        previous_timestamp = timestamp

def test_decoder_binary_exists():
    binary_path = "/home/user/decoder"
    assert os.path.exists(binary_path), f"Compiled binary {binary_path} does not exist."
    assert os.path.isfile(binary_path), f"{binary_path} is not a file."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_investigation_json():
    report_path = "/home/user/investigation.json"
    assert os.path.exists(report_path), f"Report file {report_path} does not exist."
    assert os.path.isfile(report_path), f"{report_path} is not a file."

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} does not contain valid JSON.")

    expected_keys = {"reconstructed_lines", "convergence_key", "suspicious_file"}
    missing_keys = expected_keys - set(report.keys())
    assert not missing_keys, f"Report is missing keys: {missing_keys}"

    assert report["reconstructed_lines"] == 30000, \
        f"Expected reconstructed_lines to be 30000, got {report['reconstructed_lines']}."

    expected_key = "SUCCESS_KEY: CONVERGED_0x7F8B"
    assert report["convergence_key"] == expected_key, \
        f"Expected convergence_key to be '{expected_key}', got '{report['convergence_key']}'."

    expected_file = "/etc/.hidden_bind_shell.conf"
    assert report["suspicious_file"] == expected_file, \
        f"Expected suspicious_file to be '{expected_file}', got '{report['suspicious_file']}'."