# test_final_state.py

import os
import json
import subprocess
import pytest

BINARY_PATH = "/home/user/kg_filter"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"
FINAL_REPORT_PATH = "/home/user/final_report.json"

def test_binary_exists_and_executable():
    assert os.path.isfile(BINARY_PATH), f"Compiled binary not found at {BINARY_PATH}"
    assert os.access(BINARY_PATH, os.X_OK), f"Binary at {BINARY_PATH} is not executable"

def test_adversarial_corpus_filter():
    # Test evil corpus
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    evil_bypassed = []
    for fpath in evil_files:
        result = subprocess.run([BINARY_PATH, fpath], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(fpath))

    # Test clean corpus
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    clean_rejected = []
    for fpath in clean_files:
        result = subprocess.run([BINARY_PATH, fpath], capture_output=True)
        if result.returncode != 0:
            clean_rejected.append(os.path.basename(fpath))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_rejected:
        errors.append(f"{len(clean_rejected)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_rejected)}")

    assert not errors, "Adversarial corpus filtering failed:\n" + "\n".join(errors)

def test_final_report():
    assert os.path.isfile(FINAL_REPORT_PATH), f"Final report not found at {FINAL_REPORT_PATH}"
    with open(FINAL_REPORT_PATH, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Final report at {FINAL_REPORT_PATH} is not valid JSON")

    assert "top_node_graph_001" in report, "Key 'top_node_graph_001' missing in final report"
    assert str(report["top_node_graph_001"]) == "73", f"Expected top_node_graph_001 to be '73', got {report['top_node_graph_001']}"