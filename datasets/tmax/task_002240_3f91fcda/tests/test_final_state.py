# test_final_state.py

import os
import glob
import subprocess
import tempfile
import csv
import pytest

def test_rust_binary_compiled_and_run():
    binary_path = "/app/dep-analyzer-core/target/release/dep-analyzer-core"
    assert os.path.isfile(binary_path), f"Rust binary not found at {binary_path}. Did 'cargo build --release' succeed?"

    # Verify the binary is executable
    assert os.access(binary_path, os.X_OK), f"Rust binary at {binary_path} is not executable."

    # The task requires running the binary and outputting to /home/user/rust_output.log
    output_log = "/home/user/rust_output.log"
    assert os.path.isfile(output_log), f"Rust output log not found at {output_log}."
    assert os.path.getsize(output_log) > 0, f"Rust output log at {output_log} is empty."

def test_classifier_script_exists():
    script_path = "/home/user/classifier.py"
    assert os.path.isfile(script_path), f"Classifier script not found at {script_path}."

def test_adversarial_corpus_classification():
    script_path = "/home/user/classifier.py"
    assert os.path.isfile(script_path), f"Classifier script missing: {script_path}"

    evil_dir = "/home/user/corpora/evil"
    clean_dir = "/home/user/corpora/clean"

    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))
    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))

    assert len(evil_files) > 0, f"No evil files found in {evil_dir}"
    assert len(clean_files) > 0, f"No clean files found in {clean_dir}"

    evil_bypassed = []
    clean_modified = []

    with tempfile.TemporaryDirectory() as tmpdir:
        temp_out = os.path.join(tmpdir, "out.txt")

        # Test Evil Corpus
        for evil_file in evil_files:
            try:
                subprocess.run(
                    ["python3", script_path, evil_file, temp_out],
                    check=True,
                    capture_output=True,
                    timeout=5
                )
                if os.path.exists(temp_out):
                    with open(temp_out, "r") as f:
                        result = f.read().strip()
                    if result != "EVIL":
                        evil_bypassed.append(os.path.basename(evil_file))
                else:
                    evil_bypassed.append(os.path.basename(evil_file))
            except Exception:
                evil_bypassed.append(os.path.basename(evil_file))

        # Test Clean Corpus
        for clean_file in clean_files:
            try:
                subprocess.run(
                    ["python3", script_path, clean_file, temp_out],
                    check=True,
                    capture_output=True,
                    timeout=5
                )
                if os.path.exists(temp_out):
                    with open(temp_out, "r") as f:
                        result = f.read().strip()
                    if result != "CLEAN":
                        clean_modified.append(os.path.basename(clean_file))
                else:
                    clean_modified.append(os.path.basename(clean_file))
            except Exception:
                clean_modified.append(os.path.basename(clean_file))

    error_msg = []
    if evil_bypassed:
        error_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msg.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")

    assert not error_msg, " | ".join(error_msg)

def test_csv_results_exist():
    csv_path = "/home/user/classification_results.csv"
    assert os.path.isfile(csv_path), f"Classification results CSV not found at {csv_path}."

    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "Classification results CSV is empty."