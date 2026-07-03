# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_filter_docs_script_exists_and_executable():
    script_path = "/home/user/filter_docs.sh"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_clean_corpus_accepted():
    script_path = "/home/user/filter_docs.sh"
    clean_dir = "/home/user/test_data/clean"
    clean_files = glob.glob(os.path.join(clean_dir, "*.docbundle"))

    assert len(clean_files) > 0, "No clean files found."

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run([script_path, filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(failed_files)}")

def test_evil_corpus_rejected():
    script_path = "/home/user/filter_docs.sh"
    evil_dir = "/home/user/test_data/evil"
    evil_files = glob.glob(os.path.join(evil_dir, "*.docbundle"))

    assert len(evil_files) > 0, "No evil files found."

    bypassed_files = []
    for filepath in evil_files:
        result = subprocess.run([script_path, filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            bypassed_files.append(os.path.basename(filepath))

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(bypassed_files)}")