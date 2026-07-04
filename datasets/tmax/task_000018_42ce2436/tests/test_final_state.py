# test_final_state.py
import os
import subprocess
import pytest

def test_filter_signals_script_exists():
    assert os.path.isfile('/home/user/filter_signals.py'), "The script /home/user/filter_signals.py does not exist."

def test_evil_corpus_rejected():
    evil_dir = '/app/corpus/evil'
    log_file = '/home/user/evil_rejected.log'

    # Run the student's script
    result = subprocess.run(
        ['mpiexec', '--allow-run-as-root', '-n', '4', 'python', '/home/user/filter_signals.py', evil_dir, log_file],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Script failed on evil corpus. Return code {result.returncode}.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

    assert os.path.isfile(log_file), f"Log file {log_file} was not created."

    with open(log_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_files = {f"evil_{i:03d}.npy" for i in range(100)}
    actual_files = set(lines)

    missing = expected_files - actual_files
    extra = actual_files - expected_files

    assert len(missing) == 0, f"{len(missing)} of 100 evil bypassed. Missing in log: {list(missing)[:5]}"
    assert len(extra) == 0, f"Extra files in evil log: {list(extra)[:5]}"

def test_clean_corpus_preserved():
    clean_dir = '/app/corpus/clean'
    log_file = '/home/user/clean_rejected.log'

    # Run the student's script
    result = subprocess.run(
        ['mpiexec', '--allow-run-as-root', '-n', '4', 'python', '/home/user/filter_signals.py', clean_dir, log_file],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Script failed on clean corpus. Return code {result.returncode}.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

    if not os.path.exists(log_file):
        # If it doesn't exist, it means 0 lines, which is perfect
        return

    with open(log_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 0, f"{len(lines)} of 100 clean modified/rejected. Offending files: {lines[:5]}"