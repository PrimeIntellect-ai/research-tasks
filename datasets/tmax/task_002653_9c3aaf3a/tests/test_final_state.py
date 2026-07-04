# test_final_state.py

import os
import re
import pytest

def test_results_file_exists_and_correct():
    results_file = "/home/user/profile_results.txt"
    assert os.path.isfile(results_file), f"The results file {results_file} was not generated. Did you run the script?"

    with open(results_file, "r") as f:
        content = f.read().strip()

    assert content == "Total: 550", f"Expected 'Total: 550' in {results_file}, but got '{content}'"

def test_sh_file_fixed():
    sh_file = "/home/user/profile_run.sh"
    assert os.path.isfile(sh_file), f"Missing file: {sh_file}"

    with open(sh_file, "r") as f:
        content = f.read()

    assert "METRICS_FILE" in content, "The environment variable in profile_run.sh was not corrected to METRICS_FILE"
    assert "METRIC_FILE" not in content or "export METRICS_FILE=" in content, "The typo METRIC_FILE is still present or not fixed properly."

def test_c_file_fixed():
    c_file = "/home/user/aggregate_stats.c"
    assert os.path.isfile(c_file), f"Missing file: {c_file}"

    with open(c_file, "r") as f:
        content = f.read()

    # The user should have changed count <= 10 to count < 10 (or similar logic)
    # Just check that count <= 10 is no longer there, and count < 10 is present, 
    # or that they changed the array size. The simplest fix is changing <= to <.
    assert "count <= 10" not in content, "The off-by-one error 'count <= 10' is still present in aggregate_stats.c"

    # We can be a bit flexible, but checking for the presence of the bug removal is usually enough
    # Let's ensure they didn't just delete the loop
    assert "while" in content and "fscanf" in content, "The reading loop was removed from aggregate_stats.c"