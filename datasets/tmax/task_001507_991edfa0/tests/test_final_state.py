# test_final_state.py

import os
import re
import pytest

def test_results_files_exist():
    """Ensure the user saved the results to the specified files."""
    assert os.path.isfile("/home/user/clean_results.txt"), "/home/user/clean_results.txt is missing"
    assert os.path.isfile("/home/user/evil_results.txt"), "/home/user/evil_results.txt is missing"

def test_clean_corpus_accepted():
    """Ensure all instances in the clean corpus are accepted."""
    with open("/home/user/clean_results.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 0, "clean_results.txt is empty"

    rejected = []
    for line in lines:
        if not line.endswith("ACCEPT"):
            rejected.append(line)

    if rejected:
        pytest.fail(f"{len(rejected)} of {len(lines)} clean instances modified/rejected. Examples: {rejected[:5]}")

def test_evil_corpus_rejected():
    """Ensure all instances in the evil corpus are rejected."""
    with open("/home/user/evil_results.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 0, "evil_results.txt is empty"

    accepted = []
    for line in lines:
        if not line.endswith("REJECT"):
            accepted.append(line)

    if accepted:
        pytest.fail(f"{len(accepted)} of {len(lines)} evil instances bypassed/accepted. Examples: {accepted[:5]}")

def test_benchmark_script_exists():
    """Ensure the benchmark bash script was created."""
    assert os.path.isfile("/home/user/benchmark.sh"), "/home/user/benchmark.sh is missing"
    assert os.access("/home/user/benchmark.sh", os.X_OK), "/home/user/benchmark.sh is not executable"