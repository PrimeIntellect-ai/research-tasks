# test_final_state.py

import os
import subprocess
import pytest

def test_filter_edm_on_corpora():
    script_path = "/home/user/filter_edm.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    evil_corpus_path = "/app/corpora/evil/"
    clean_corpus_path = "/app/corpora/clean/"

    evil_files = [os.path.join(evil_corpus_path, f) for f in os.listdir(evil_corpus_path) if f.endswith('.pdist')]
    clean_files = [os.path.join(clean_corpus_path, f) for f in os.listdir(clean_corpus_path) if f.endswith('.pdist')]

    assert len(evil_files) > 0, "No files found in evil corpus."
    assert len(clean_files) > 0, "No files found in clean corpus."

    evil_bypassed = []
    for evil_file in evil_files:
        result = subprocess.run(["python3", script_path, evil_file], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(evil_file))

    clean_modified = []
    for clean_file in clean_files:
        result = subprocess.run(["python3", script_path, clean_file], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(clean_file))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")

    assert not errors, " | ".join(errors)