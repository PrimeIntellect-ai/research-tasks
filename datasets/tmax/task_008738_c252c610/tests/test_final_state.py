# test_final_state.py

import os
import subprocess
import pytest

def test_diagnostics_file_and_contents():
    diag_file = "/home/user/diagnostics.txt"
    assert os.path.isfile(diag_file), f"Diagnostics file {diag_file} does not exist."

    with open(diag_file, "r") as f:
        lines = f.read().splitlines()

    data = {}
    for line in lines:
        if "=" in line:
            key, val = line.split("=", 1)
            data[key.strip()] = val.strip()

    assert "BAD_COMMIT" in data, "Key 'BAD_COMMIT' is missing from diagnostics.txt"
    assert "DIVERGENCE_ITERATION" in data, "Key 'DIVERGENCE_ITERATION' is missing from diagnostics.txt"

    repo_dir = "/home/user/markov_solver"
    assert os.path.isdir(repo_dir), f"Repository directory {repo_dir} does not exist."

    # Dynamically find the bad commit hash from git history
    result = subprocess.run(
        ["git", "log", "--grep=Optimize inner loop calculation", "--format=%H"],
        cwd=repo_dir,
        capture_output=True,
        text=True,
        check=True
    )
    expected_hash = result.stdout.strip()
    assert expected_hash, "Could not find the expected commit with message 'Optimize inner loop calculation' in git history."

    # Validate BAD_COMMIT
    actual_hash = data["BAD_COMMIT"]
    assert actual_hash == expected_hash, f"BAD_COMMIT is incorrect. Expected {expected_hash}, got {actual_hash}"

    # Validate DIVERGENCE_ITERATION
    # The sum of next_state drops below 0.99 at iteration 1 (0-indexed).
    actual_iteration = data["DIVERGENCE_ITERATION"]
    assert actual_iteration == "1", f"DIVERGENCE_ITERATION is incorrect. Expected 1, got {actual_iteration}"