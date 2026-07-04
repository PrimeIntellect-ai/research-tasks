# test_final_state.py

import os
import glob
import subprocess

def test_libinfer_ops_compiled_and_benchmarked():
    baseline_file = "/app/libinfer_ops-1.2.0/baseline_perf.txt"
    assert os.path.isfile(baseline_file), f"Expected benchmark output file {baseline_file} does not exist. Did you run ./benchmark_infer?"

    with open(baseline_file, "r") as f:
        content = f.read()
    assert "TRACKER_OVERHEAD_MS" in content, f"File {baseline_file} does not contain the expected benchmark output."

def test_sanitizer_binary_exists():
    binary_path = "/home/user/sanitizer"
    assert os.path.isfile(binary_path), f"Sanitizer binary not found at {binary_path}. Did you compile it?"
    assert os.access(binary_path, os.X_OK), f"Sanitizer binary at {binary_path} is not executable."

def test_sanitizer_adversarial_corpus():
    binary_path = "/home/user/sanitizer"
    evil_dir = "/app/corpora/evil"
    clean_dir = "/app/corpora/clean"

    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))
    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))

    assert len(evil_files) > 0, "Evil corpus is empty or missing."
    assert len(clean_files) > 0, "Clean corpus is empty or missing."

    evil_bypassed = []
    for f in evil_files:
        result = subprocess.run([binary_path, f], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(f))

    clean_modified = []
    for f in clean_files:
        result = subprocess.run([binary_path, f], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(f))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: " + ", ".join(evil_bypassed[:10]) + ("..." if len(evil_bypassed) > 10 else ""))
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified/rejected: " + ", ".join(clean_modified[:10]) + ("..." if len(clean_modified) > 10 else ""))

    if error_msgs:
        assert False, " | ".join(error_msgs)