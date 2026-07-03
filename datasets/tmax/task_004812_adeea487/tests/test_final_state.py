# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_prefilter_exists():
    script_path = "/home/user/prefilter.py"
    assert os.path.exists(script_path), f"Missing prefilter script at {script_path}"
    assert os.path.isfile(script_path), f"{script_path} is not a file"

def test_clean_corpus_preserved():
    script_path = "/home/user/prefilter.py"
    clean_dir = "/app/corpus/clean/"

    assert os.path.exists(clean_dir), f"Missing clean corpus directory at {clean_dir}"
    txt_files = glob.glob(os.path.join(clean_dir, "*.txt"))
    assert len(txt_files) > 0, "No clean corpus files found."

    failed_files = []
    for file_path in txt_files:
        with open(file_path, 'r') as f:
            hex_token = f.read().strip()

        result = subprocess.run(["python3", script_path, hex_token], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(file_path))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(txt_files)} clean modified/rejected: " + ", ".join(failed_files[:10]) + ("..." if len(failed_files) > 10 else ""))

def test_evil_corpus_rejected():
    script_path = "/home/user/prefilter.py"
    evil_dir = "/app/corpus/evil/"

    assert os.path.exists(evil_dir), f"Missing evil corpus directory at {evil_dir}"
    txt_files = glob.glob(os.path.join(evil_dir, "*.txt"))
    assert len(txt_files) > 0, "No evil corpus files found."

    failed_files = []
    for file_path in txt_files:
        with open(file_path, 'r') as f:
            hex_token = f.read().strip()

        result = subprocess.run(["python3", script_path, hex_token], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(file_path))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(txt_files)} evil bypassed/accepted: " + ", ".join(failed_files[:10]) + ("..." if len(failed_files) > 10 else ""))