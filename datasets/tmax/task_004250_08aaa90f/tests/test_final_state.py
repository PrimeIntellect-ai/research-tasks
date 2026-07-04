# test_final_state.py
import os
import glob
import subprocess
import pytest

def test_vendored_package_fixed():
    graph_go_path = "/app/graph/graph.go"
    assert os.path.isfile(graph_go_path), f"File {graph_go_path} is missing."
    with open(graph_go_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "package graph" in content and "package grraph" not in content, (
        f"The typo 'package grraph' in {graph_go_path} was not correctly fixed."
    )

def test_adversarial_corpus():
    classifier_path = "/home/user/classifier.go"
    assert os.path.isfile(classifier_path), f"Classifier program not found at {classifier_path}"

    clean_dir = "/home/user/corpora/clean"
    evil_dir = "/home/user/corpora/evil"

    clean_csvs = glob.glob(os.path.join(clean_dir, "*.csv"))
    evil_csvs = glob.glob(os.path.join(evil_dir, "*.csv"))

    assert len(clean_csvs) > 0, "No clean CSV files found in truth corpus."
    assert len(evil_csvs) > 0, "No evil CSV files found in truth corpus."

    clean_failures = []
    for csv_file in clean_csvs:
        result = subprocess.run(["go", "run", classifier_path, csv_file], capture_output=True, text=True)
        if result.returncode != 0 or "CLEAN" not in result.stdout:
            clean_failures.append(os.path.basename(csv_file))

    evil_failures = []
    for csv_file in evil_csvs:
        result = subprocess.run(["go", "run", classifier_path, csv_file], capture_output=True, text=True)
        if result.returncode != 1 or "EVIL" not in result.stdout:
            evil_failures.append(os.path.basename(csv_file))

    error_messages = []
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_csvs)} clean modified/rejected: {', '.join(clean_failures)}")
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_csvs)} evil bypassed: {', '.join(evil_failures)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))