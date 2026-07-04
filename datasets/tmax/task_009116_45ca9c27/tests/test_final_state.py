# test_final_state.py

import os
import json
import pytest

def test_critical_alerts_log_exists_and_line_count():
    """Test that critical_alerts.log exists and contains exactly 42 lines."""
    log_path = "/home/user/parsed/critical_alerts.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist."

    with open(log_path, 'r') as f:
        lines = f.readlines()

    assert len(lines) == 42, f"Expected 42 lines in {log_path}, but found {len(lines)}."

def test_critical_alerts_log_content():
    """Test that critical_alerts.log contains valid JSON and only CRITICAL severity."""
    log_path = "/home/user/parsed/critical_alerts.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist."

    with open(log_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                pytest.fail(f"Line {line_num} in {log_path} is not valid JSON: {line.strip()}")

            assert "severity" in record, f"Line {line_num} missing 'severity' key."
            assert record["severity"] == "CRITICAL", f"Line {line_num} has severity '{record['severity']}', expected 'CRITICAL'."

def test_split_files_exist_and_line_counts():
    """Test that the split files exist with the correct names and line counts."""
    split_dir = "/home/user/parsed/split"
    assert os.path.isdir(split_dir), f"Directory {split_dir} does not exist."

    expected_files = {
        "crit_part_aa": 10,
        "crit_part_ab": 10,
        "crit_part_ac": 10,
        "crit_part_ad": 10,
        "crit_part_ae": 2
    }

    for filename, expected_lines in expected_files.items():
        file_path = os.path.join(split_dir, filename)
        assert os.path.isfile(file_path), f"Expected split file {file_path} does not exist."

        with open(file_path, 'r') as f:
            lines = f.readlines()
        assert len(lines) == expected_lines, f"Expected {expected_lines} lines in {filename}, but found {len(lines)}."

def test_symlink_latest_alert_part():
    """Test that the symlink exists and points to the last split chunk file."""
    symlink_path = "/home/user/parsed/latest_alert_part"
    expected_target = "/home/user/parsed/split/crit_part_ae"

    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."

    target = os.readlink(symlink_path)
    # The task asks for absolute path
    assert target == expected_target, f"Symlink points to {target}, expected {expected_target}."