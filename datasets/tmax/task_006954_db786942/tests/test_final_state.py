# test_final_state.py

import os
import pytest

def test_critical_summary_exists_and_content_correct():
    summary_path = "/home/user/critical_summary.log"
    assert os.path.isfile(summary_path), f"The file {summary_path} does not exist."

    expected_lines = [
        "[CRITICAL] Database connection lost",
        "[CRITICAL] Disk space critically low on /dev/sda1",
        "[CRITICAL] Unhandled exception in worker thread"
    ]

    with open(summary_path, 'r') as f:
        content = f.read().strip().splitlines()

    assert content == expected_lines, "The content of critical_summary.log does not match the expected extracted [CRITICAL] lines."

def test_script_exists():
    script_path = "/home/user/extract_critical.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_script_atomic_write_and_gzip():
    script_path = "/home/user/extract_critical.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

    with open(script_path, 'r') as f:
        code = f.read()

    assert "gzip" in code, "The script does not appear to use the 'gzip' module."

    has_atomic_move = any(func in code for func in ["os.replace", "os.rename", "shutil.move"])
    assert has_atomic_move, "The script does not appear to use an atomic write pattern (os.replace, os.rename, or shutil.move)."