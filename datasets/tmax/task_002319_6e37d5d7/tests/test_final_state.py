# test_final_state.py
import os
import subprocess
import pytest
import glob

def test_json11_library_built():
    assert os.path.isfile('/app/json11/libjson11.a'), "The static library /app/json11/libjson11.a was not built."

def test_artifact_validator_executable():
    validator_path = '/home/user/artifact_validator'
    assert os.path.isfile(validator_path), f"The validator {validator_path} does not exist."
    assert os.access(validator_path, os.X_OK), f"The validator {validator_path} is not executable."

def test_validator_adversarial_corpus():
    validator_path = '/home/user/artifact_validator'
    clean_dir = '/app/corpora/clean/'
    evil_dir = '/app/corpora/evil/'

    clean_files = glob.glob(os.path.join(clean_dir, '*.json'))
    evil_files = glob.glob(os.path.join(evil_dir, '*.json'))

    assert len(clean_files) > 0, "No clean files found in corpus."
    assert len(evil_files) > 0, "No evil files found in corpus."

    bypassed_evil = []
    modified_clean = []

    for cf in clean_files:
        result = subprocess.run([validator_path, cf], capture_output=True)
        if result.returncode != 0:
            modified_clean.append(os.path.basename(cf))

    for ef in evil_files:
        result = subprocess.run([validator_path, ef], capture_output=True)
        if result.returncode == 0:
            bypassed_evil.append(os.path.basename(ef))

    error_msgs = []
    if bypassed_evil:
        error_msgs.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        error_msgs.append(f"{len(modified_clean)} of {len(clean_files)} clean modified (rejected): {', '.join(modified_clean)}")

    assert not error_msgs, " / ".join(error_msgs)

def test_run_validation_script_results():
    accepted_dir = '/home/user/accepted'
    rejected_dir = '/home/user/rejected'

    assert os.path.isdir(accepted_dir), f"Directory {accepted_dir} does not exist."
    assert os.path.isdir(rejected_dir), f"Directory {rejected_dir} does not exist."

    clean_dir = '/app/corpora/clean'
    evil_dir = '/app/corpora/evil'

    expected_clean = set(os.listdir(clean_dir))
    expected_evil = set(os.listdir(evil_dir))

    actual_accepted = set(os.listdir(accepted_dir))
    actual_rejected = set(os.listdir(rejected_dir))

    assert actual_accepted == expected_clean, f"Accepted directory contents mismatch. Expected: {expected_clean}, Found: {actual_accepted}"
    assert actual_rejected == expected_evil, f"Rejected directory contents mismatch. Expected: {expected_evil}, Found: {actual_rejected}"