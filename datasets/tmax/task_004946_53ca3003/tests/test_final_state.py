# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_anomaly_solver_fixed():
    path = "/home/user/anomaly_solver.py"
    assert os.path.isfile(path), f"Missing anomaly_solver.py file at {path}"

    with open(path, 'r') as f:
        content = f.read()

    assert "0.997" in content, "anomaly_solver.py does not contain the corrected decay constant (0.997)"
    assert "N - 2" in content, "anomaly_solver.py does not contain the corrected denominator (N - 2)"
    assert "0.85" not in content, "anomaly_solver.py still contains the flawed decay constant (0.85)"
    assert "N - 1" not in content, "anomaly_solver.py still contains the flawed denominator (N - 1)"

def test_incident_report_log():
    path = "/home/user/incident_report.log"
    assert os.path.isfile(path), f"Missing incident_report.log file at {path}"

    with open(path, 'r') as f:
        content = f.read().strip()

    assert content == "0.997", f"incident_report.log does not contain exactly '0.997', found: '{content}'"

def test_classifier_corpus():
    classifier_path = "/home/user/classifier.py"
    assert os.path.isfile(classifier_path), f"Missing classifier script at {classifier_path}"

    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    clean_files = glob.glob(os.path.join(clean_dir, "*"))
    evil_files = glob.glob(os.path.join(evil_dir, "*"))

    assert len(clean_files) > 0, "No files found in clean corpus"
    assert len(evil_files) > 0, "No files found in evil corpus"

    clean_failures = []
    for cf in clean_files:
        if not os.path.isfile(cf): continue
        result = subprocess.run(["python3", classifier_path, cf], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(cf))

    evil_failures = []
    for ef in evil_files:
        if not os.path.isfile(ef): continue
        result = subprocess.run(["python3", classifier_path, ef], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(os.path.basename(ef))

    error_messages = []
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/flagged: {', '.join(clean_failures)}")
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")

    assert not error_messages, "Classifier failed on corpus:\n" + "\n".join(error_messages)