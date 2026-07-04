# test_final_state.py

import os
import subprocess
import pytest

CLEAN_CORPUS_DIR = "/app/corpus/clean/"
EVIL_CORPUS_DIR = "/app/corpus/evil/"
DETECTOR_SCRIPT = "/home/user/detector.py"
PLOT_FILE = "/home/user/svd_plot.png"

def test_detector_exists():
    assert os.path.isfile(DETECTOR_SCRIPT), f"Detector script missing: {DETECTOR_SCRIPT}"

def test_plot_exists():
    assert os.path.isfile(PLOT_FILE), f"Plot file missing: {PLOT_FILE}"
    assert os.path.getsize(PLOT_FILE) > 0, f"Plot file is empty: {PLOT_FILE}"

def test_detector_clean_corpus():
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith(".npy")]
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_clean = []
    for f in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, f)
        result = subprocess.run(["python3", DETECTOR_SCRIPT, filepath], capture_output=True, text=True)
        if result.returncode != 0 or result.stdout.strip() != "CLEAN":
            failed_clean.append(f)

    assert len(failed_clean) == 0, f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected. Offending files: {failed_clean}"

def test_detector_evil_corpus():
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith(".npy")]
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_evil = []
    for f in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, f)
        result = subprocess.run(["python3", DETECTOR_SCRIPT, filepath], capture_output=True, text=True)
        if result.returncode != 0 or result.stdout.strip() != "EVIL":
            failed_evil.append(f)

    assert len(failed_evil) == 0, f"{len(failed_evil)} of {len(evil_files)} evil bypassed. Offending files: {failed_evil}"