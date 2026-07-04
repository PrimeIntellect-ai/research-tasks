# test_final_state.py
import json
import os
import subprocess
import time
import pytest

def test_profile_notes_exists_and_correct():
    notes_path = "/home/user/bio_profiling/profile_notes.txt"
    assert os.path.isfile(notes_path), f"File missing: {notes_path}"

    with open(notes_path, "r") as f:
        first_line = f.readline().strip().lower()

    assert "integrate_efficiency" in first_line or "calculate_tm" in first_line, \
        f"The first line of profile_notes.txt must identify the slowest function. Found: '{first_line}'"

def test_optimized_script_execution_time_and_success():
    script_path = "/home/user/bio_profiling/optimized_primer_sim.py"
    assert os.path.isfile(script_path), f"Optimized script missing: {script_path}"

    start_time = time.time()
    proc = subprocess.run(
        ["python3", script_path],
        capture_output=True,
        text=True
    )
    elapsed = time.time() - start_time

    assert proc.returncode == 0, f"Optimized script failed with exit code {proc.returncode}.\nStderr: {proc.stderr}"
    assert elapsed < 2.0, f"Optimized script took {elapsed:.2f} seconds, which is strictly >= 2.0 seconds limit."

def test_results_json_accuracy():
    results_path = "/home/user/bio_profiling/results.json"
    expected_path = "/home/user/bio_profiling/expected_results.json"

    assert os.path.isfile(results_path), f"Results file missing: {results_path}"
    assert os.path.isfile(expected_path), f"Expected results file missing: {expected_path}"

    with open(expected_path, "r") as f:
        expected = json.load(f)

    with open(results_path, "r") as f:
        actual = json.load(f)

    for key in expected:
        assert key in actual, f"Sequence key '{key}' missing in results.json"

        for metric in ["tm", "efficiency"]:
            assert metric in actual[key], f"Metric '{metric}' missing for sequence '{key}'"
            exp_val = expected[key][metric]
            act_val = actual[key][metric]

            # Calculate relative difference
            rel_diff = abs(exp_val - act_val) / max(1e-9, abs(exp_val))
            assert rel_diff <= 1e-4, \
                f"Value mismatch for {key} {metric}: expected {exp_val}, got {act_val} (rel diff: {rel_diff:.2e} > 1e-4)"