# test_final_state.py
import os
import glob
import subprocess
import pytest

def test_compliance_filter():
    script_path = '/home/user/compliance_filter.py'
    db_path = '/app/data/corp.db'

    assert os.path.exists(script_path), f"Script not found at {script_path}"

    evil_corpus_dir = '/app/corpus/evil/'
    clean_corpus_dir = '/app/corpus/clean/'

    evil_files = glob.glob(os.path.join(evil_corpus_dir, '*.json'))
    clean_files = glob.glob(os.path.join(clean_corpus_dir, '*.json'))

    assert len(evil_files) > 0, "No evil corpus files found."
    assert len(clean_files) > 0, "No clean corpus files found."

    evil_bypassed = []
    for fpath in evil_files:
        cmd = ['python3', script_path, '--db', db_path, '--tx', fpath]
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(fpath))

    clean_modified = []
    for fpath in clean_files:
        cmd = ['python3', script_path, '--db', db_path, '--tx', fpath]
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(fpath))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))