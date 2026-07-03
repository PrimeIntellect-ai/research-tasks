# test_final_state.py

import os
import subprocess
import pytest
import glob

def test_vendor_fixed():
    csv_go_path = "/app/vendor/gocsv/csv.go"
    assert os.path.isfile(csv_go_path), f"File {csv_go_path} is missing."
    with open(csv_go_path, "r") as f:
        content = f.read()
    assert 'panic("UNAUTHORIZED MODIFICATION")' not in content, f"Perturbation still exists in {csv_go_path}."

def test_adversarial_corpus_validate():
    clean_corpus_path = "/home/user/data/clean_corpus"
    evil_corpus_path = "/home/user/data/evil_corpus"
    pipeline_dir = "/home/user/pipeline"

    assert os.path.isdir(clean_corpus_path), f"Clean corpus directory {clean_corpus_path} is missing."
    assert os.path.isdir(evil_corpus_path), f"Evil corpus directory {evil_corpus_path} is missing."
    assert os.path.isdir(pipeline_dir), f"Pipeline directory {pipeline_dir} is missing."

    clean_files = glob.glob(os.path.join(clean_corpus_path, "*.csv"))
    evil_files = glob.glob(os.path.join(evil_corpus_path, "*.csv"))

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failures = []
    evil_failures = []

    for f in clean_files:
        result = subprocess.run(
            ["go", "run", "main.go", "validate", f],
            cwd=pipeline_dir,
            capture_output=True
        )
        if result.returncode != 0:
            clean_failures.append(os.path.basename(f))

    for f in evil_files:
        result = subprocess.run(
            ["go", "run", "main.go", "validate", f],
            cwd=pipeline_dir,
            capture_output=True
        )
        if result.returncode != 1:
            evil_failures.append(os.path.basename(f))

    error_messages = []
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")

    assert not error_messages, " | ".join(error_messages)