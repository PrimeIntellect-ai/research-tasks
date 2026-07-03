# test_final_state.py

import os
import glob
import pytest

def test_critical_events_file():
    """Verify the critical events output file exists and has the correct content."""
    output_file = "/home/user/critical_events.txt"
    assert os.path.exists(output_file), f"Output file {output_file} does not exist."

    with open(output_file, "r") as f:
        lines = f.readlines()

    assert len(lines) == 60, f"Expected 60 critical event lines, but found {len(lines)}."

    for i, line in enumerate(lines):
        assert "[CRITICAL]" in line, f"Line {i+1} does not contain '[CRITICAL]': {line.strip()}"

def test_archived_files():
    """Verify all 20 log files have been renamed to .archived.gz."""
    raw_logs_dir = "/home/user/backup_data/raw_logs/"
    archived_files = glob.glob(os.path.join(raw_logs_dir, "*.archived.gz"))
    assert len(archived_files) == 20, f"Expected 20 .archived.gz files, found {len(archived_files)}."

def test_no_log_gz_files():
    """Verify no .log.gz files remain in the raw logs directory."""
    raw_logs_dir = "/home/user/backup_data/raw_logs/"
    log_files = glob.glob(os.path.join(raw_logs_dir, "*.log.gz"))
    assert len(log_files) == 0, f"Found {len(log_files)} .log.gz files remaining, expected 0."

def test_script_requirements():
    """Verify the script exists and uses concurrency and fcntl."""
    script_file = "/home/user/archive_processor.py"
    assert os.path.exists(script_file), f"Script file {script_file} does not exist."

    with open(script_file, "r") as f:
        content = f.read()

    assert "fcntl" in content, "The script does not appear to use 'fcntl' for file locking."

    has_concurrency = "multiprocessing" in content or "concurrent.futures" in content
    assert has_concurrency, "The script does not appear to use 'multiprocessing' or 'concurrent.futures'."