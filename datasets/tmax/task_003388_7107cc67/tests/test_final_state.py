# test_final_state.py

import os
import subprocess
import pytest
from decimal import Decimal, getcontext

# Set high precision for decimal calculations to match bc -l
getcontext().prec = 50

def test_git_forensics_recovered_file():
    env_file = "/home/user/pipeline-config/math_thresholds.env"
    assert os.path.exists(env_file), f"Recovered file not found at {env_file}"

    with open(env_file, 'r') as f:
        content = f.read()

    assert "PRECISION_SCALE=20" in content, "Missing PRECISION_SCALE=20 in recovered file"
    assert "MAX_LATENCY_THRESHOLD=999.999" in content, "Missing MAX_LATENCY_THRESHOLD=999.999 in recovered file"

def test_vendored_package_aggregation_result():
    result_file = "/home/user/aggregated_result.txt"
    test_logs_dir = "/home/user/test_logs"

    assert os.path.exists(result_file), f"Aggregated result file not found at {result_file}"

    # Calculate the expected sum using Python's Decimal for precision
    expected_sum = Decimal('0')
    for root, _, files in os.walk(test_logs_dir):
        for filename in files:
            filepath = os.path.join(root, filename)
            with open(filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    # The script sums the first column
                    parts = line.split()
                    if parts:
                        try:
                            val = Decimal(parts[0])
                            expected_sum += val
                        except Exception:
                            pass

    with open(result_file, 'r') as f:
        actual_result_str = f.read().strip()

    assert actual_result_str, "Aggregated result file is empty"

    try:
        actual_sum = Decimal(actual_result_str)
    except Exception:
        pytest.fail(f"Aggregated result '{actual_result_str}' is not a valid number")

    # Compare with a small tolerance or exact match
    # bc -l usually formats without trailing zeros, but Decimal might keep them.
    # We compare their mathematical equivalence.
    assert expected_sum == actual_sum, f"Aggregated sum mismatch. Expected {expected_sum}, got {actual_sum}"

def test_adversarial_corpus_sanitization():
    sanitize_script = "/home/user/sanitize.sh"
    assert os.path.exists(sanitize_script), f"Sanitize script not found at {sanitize_script}"

    clean_corpus_dir = "/home/user/corpora/clean"
    evil_corpus_dir = "/home/user/corpora/evil"

    clean_files = [os.path.join(clean_corpus_dir, f) for f in os.listdir(clean_corpus_dir) if os.path.isfile(os.path.join(clean_corpus_dir, f))]
    evil_files = [os.path.join(evil_corpus_dir, f) for f in os.listdir(evil_corpus_dir) if os.path.isfile(os.path.join(evil_corpus_dir, f))]

    failed_clean = []
    failed_evil = []

    for fpath in clean_files:
        result = subprocess.run(["/bin/bash", sanitize_script, fpath], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(fpath))

    for fpath in evil_files:
        result = subprocess.run(["/bin/bash", sanitize_script, fpath], capture_output=True)
        if result.returncode != 1:
            failed_evil.append(os.path.basename(fpath))

    error_msgs = []
    if failed_clean:
        error_msgs.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean)}")
    if failed_evil:
        error_msgs.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed/accepted: {', '.join(failed_evil)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))