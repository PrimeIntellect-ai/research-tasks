# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_sanitizer_exists():
    path = "/home/user/sanitizer.py"
    assert os.path.isfile(path), f"sanitizer.py not found at {path}"

def test_clean_corpus():
    clean_logs_dir = "/app/clean_logs"
    clean_logs = glob.glob(os.path.join(clean_logs_dir, "*"))
    assert len(clean_logs) > 0, f"No clean logs found in {clean_logs_dir}"

    failed_files = []
    for log_file in clean_logs:
        result = subprocess.run(
            ["python3", "/home/user/sanitizer.py", log_file],
            capture_output=True,
            text=True
        )
        # Clean logs should exit with code 0
        if result.returncode != 0:
            failed_files.append(os.path.basename(log_file))

    assert not failed_files, f"{len(failed_files)} of {len(clean_logs)} clean logs modified/rejected: {', '.join(failed_files)}"

def test_evil_corpus():
    evil_logs_dir = "/app/evil_logs"
    evil_logs = glob.glob(os.path.join(evil_logs_dir, "*"))
    assert len(evil_logs) > 0, f"No evil logs found in {evil_logs_dir}"

    bypassed_files = []
    for log_file in evil_logs:
        result = subprocess.run(
            ["python3", "/home/user/sanitizer.py", log_file],
            capture_output=True,
            text=True
        )
        # Evil logs should exit with code 1 and stdout should contain the specific rule ID
        if result.returncode != 1 or "EVIL: 99B-4X2" not in result.stdout:
            bypassed_files.append(os.path.basename(log_file))

    assert not bypassed_files, f"{len(bypassed_files)} of {len(evil_logs)} evil logs bypassed: {', '.join(bypassed_files)}"