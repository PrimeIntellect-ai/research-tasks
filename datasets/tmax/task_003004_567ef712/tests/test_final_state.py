# test_final_state.py

import os
import glob
import subprocess
import stat

def test_classifier_exists_and_executable():
    executable_path = '/home/user/classifier'
    assert os.path.isfile(executable_path), f"Executable {executable_path} does not exist."

    st = os.stat(executable_path)
    is_executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, f"File {executable_path} is not executable."

def test_adversarial_corpus_classification():
    executable_path = '/home/user/classifier'
    clean_dir = '/app/corpus/clean'
    evil_dir = '/app/corpus/evil'

    clean_files = glob.glob(os.path.join(clean_dir, '*.csv'))
    evil_files = glob.glob(os.path.join(evil_dir, '*.csv'))

    assert len(clean_files) > 0, f"No clean CSV files found in {clean_dir}."
    assert len(evil_files) > 0, f"No evil CSV files found in {evil_dir}."

    failed_clean = []
    failed_evil = []

    # Test clean corpus (expected exit code 0)
    for clean_file in clean_files:
        result = subprocess.run([executable_path, clean_file], capture_output=True)
        if result.returncode != 0:
            failed_clean.append((os.path.basename(clean_file), result.returncode))

    # Test evil corpus (expected exit code 1)
    for evil_file in evil_files:
        result = subprocess.run([executable_path, evil_file], capture_output=True)
        if result.returncode != 1:
            failed_evil.append((os.path.basename(evil_file), result.returncode))

    error_messages = []
    if failed_clean:
        error_messages.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected. Offending files: " + ", ".join(f"{f} (exit {c})" for f, c in failed_clean))
    if failed_evil:
        error_messages.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed/accepted. Offending files: " + ", ".join(f"{f} (exit {c})" for f, c in failed_evil))

    if error_messages:
        assert False, " | ".join(error_messages)