# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_filter_clean_corpus():
    clean_dir = "/app/hidden_corpus/clean"
    files = glob.glob(os.path.join(clean_dir, "*"))
    assert files, f"No files found in {clean_dir}"

    failures = []
    for f in files:
        res = subprocess.run(["bash", "/home/user/filter.sh", f], capture_output=True)
        if res.returncode != 0:
            failures.append(os.path.basename(f))

    assert not failures, f"{len(failures)} of {len(files)} clean modified/rejected: {failures}"

def test_filter_evil_corpus():
    evil_dir = "/app/hidden_corpus/evil"
    files = glob.glob(os.path.join(evil_dir, "*"))
    assert files, f"No files found in {evil_dir}"

    failures = []
    for f in files:
        res = subprocess.run(["bash", "/home/user/filter.sh", f], capture_output=True)
        if res.returncode != 1:
            failures.append(os.path.basename(f))

    assert not failures, f"{len(failures)} of {len(files)} evil bypassed: {failures}"

def test_processed_output_exists():
    out_file = "/home/user/processed_output.wav"
    assert os.path.isfile(out_file), f"{out_file} does not exist. The integration script may not have run or failed."
    # Basic check for WAV header
    with open(out_file, "rb") as f:
        header = f.read(12)
        assert header.startswith(b"RIFF") and header.endswith(b"WAVE"), f"{out_file} is not a valid WAV file."