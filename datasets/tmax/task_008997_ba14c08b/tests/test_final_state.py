# test_final_state.py

import os
import json
import subprocess
import pytest

WORKSPACE_DIR = "/home/user/mlops_workspace"
COMPUTE_SCRIPT = os.path.join(WORKSPACE_DIR, "compute_retrieval.py")
TEST_SCRIPT = os.path.join(WORKSPACE_DIR, "test_accuracy.py")
RESULTS_FILE = os.path.join(WORKSPACE_DIR, "retrieved_pairs.json")

def test_scripts_exist():
    assert os.path.isfile(COMPUTE_SCRIPT), f"Missing script: {COMPUTE_SCRIPT}"
    assert os.path.isfile(TEST_SCRIPT), f"Missing test script: {TEST_SCRIPT}"

def test_results_file_exists_and_valid():
    assert os.path.isfile(RESULTS_FILE), f"Missing results file: {RESULTS_FILE}"

    with open(RESULTS_FILE, "r") as f:
        try:
            pairs = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {RESULTS_FILE} is not valid JSON.")

    assert isinstance(pairs, list), "Results should be a JSON list."

    expected_pairs = {(0, 2), (5, 11)}
    found_pairs = set()

    prev_sim = float('inf')

    for p in pairs:
        assert isinstance(p, list) and len(p) == 3, f"Each item must be a list of length 3, got: {p}"
        idx1, idx2, sim = p
        assert isinstance(idx1, int) and isinstance(idx2, int), "First two elements must be integers."
        assert isinstance(sim, (float, int)), "Third element must be a float."

        # Check ordering
        assert sim <= prev_sim, "Results are not sorted by similarity score in descending order."
        prev_sim = sim

        found_pairs.add((min(idx1, idx2), max(idx1, idx2)))
        assert sim >= 0.80, f"Similarity {sim} is less than 0.80"
        assert sim <= 1.0001, f"Similarity {sim} is greater than expected bounds"

    assert expected_pairs.issubset(found_pairs), f"Did not find expected duplicate pairs: {expected_pairs - found_pairs}"

def test_accuracy_script_passes():
    # Run pytest on the student's test script
    result = subprocess.run(
        ["pytest", TEST_SCRIPT],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"pytest {TEST_SCRIPT} failed with output:\n{result.stdout}\n{result.stderr}"