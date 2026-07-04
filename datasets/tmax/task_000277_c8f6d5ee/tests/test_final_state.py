# test_final_state.py

import os
import json
import glob
import pytest

def test_c_library_compiled():
    lib_path = "/app/lib/libcwav.so"
    assert os.path.isfile(lib_path), f"Shared library {lib_path} was not compiled."

def test_adversarial_corpus_results():
    results_path = "results.json"
    if not os.path.exists(results_path):
        results_path = "/app/results.json"

    assert os.path.exists(results_path), "results.json not found in the current working directory."

    with open(results_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("results.json is not a valid JSON file.")

    evil_dir = "/verify/hidden_corpora/evil"
    clean_dir = "/verify/hidden_corpora/clean"

    evil_files = [os.path.basename(p) for p in glob.glob(os.path.join(evil_dir, "*.cwav"))]
    clean_files = [os.path.basename(p) for p in glob.glob(os.path.join(clean_dir, "*.cwav"))]

    assert len(evil_files) > 0, "No evil corpus files found to verify against."
    assert len(clean_files) > 0, "No clean corpus files found to verify against."

    evil_bypassed = []
    for ef in evil_files:
        if results.get(ef) != "REJECT":
            evil_bypassed.append(ef)

    clean_modified = []
    for cf in clean_files:
        if results.get(cf) != "ACCEPT":
            clean_modified.append(cf)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))