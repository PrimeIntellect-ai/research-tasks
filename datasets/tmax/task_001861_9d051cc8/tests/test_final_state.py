import os
import subprocess
import glob
import pytest

def test_sanitizer_exists_and_executable():
    sanitizer_path = '/home/user/sanitizer'
    assert os.path.isfile(sanitizer_path), f"Sanitizer executable {sanitizer_path} does not exist."
    assert os.access(sanitizer_path, os.X_OK), f"Sanitizer {sanitizer_path} is not executable."

def test_sanitizer_clean_corpus():
    sanitizer_path = '/home/user/sanitizer'
    clean_dir = '/app/corpora/clean/'

    clean_files = glob.glob(os.path.join(clean_dir, '*'))
    assert len(clean_files) > 0, "No files found in clean corpus."

    failed_files = []
    for filepath in clean_files:
        with open(filepath, 'rb') as f:
            input_data = f.read()

        result = subprocess.run(
            [sanitizer_path],
            input=input_data,
            capture_output=True
        )

        if result.returncode != 0:
            failed_files.append(f"{os.path.basename(filepath)} (crashed)")
            continue

        if result.stdout != input_data:
            failed_files.append(os.path.basename(filepath))

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_files)}"

def test_sanitizer_evil_corpus():
    sanitizer_path = '/home/user/sanitizer'
    evil_dir = '/app/corpora/evil/'

    evil_files = glob.glob(os.path.join(evil_dir, '*'))
    assert len(evil_files) > 0, "No files found in evil corpus."

    failed_files = []
    for filepath in evil_files:
        with open(filepath, 'rb') as f:
            input_data = f.read()

        result = subprocess.run(
            [sanitizer_path],
            input=input_data,
            capture_output=True
        )

        if result.returncode != 0:
            # Crashing on evil input is generally bad, but if it crashes it didn't output valid records.
            # However, a robust sanitizer should exit cleanly. Let's not strict check return code here,
            # just that stdout is empty.
            pass

        if result.stdout.strip() != b"":
            failed_files.append(os.path.basename(filepath))

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil bypassed: {', '.join(failed_files)}"

def test_master_clean_log_exists():
    log_path = '/home/user/master_clean.log'
    assert os.path.isfile(log_path), f"Final output file {log_path} is missing."
    assert os.path.getsize(log_path) > 0, f"Final output file {log_path} is empty."