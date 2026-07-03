# test_final_state.py

import os
import json
import subprocess
import pytest

REPO_DIR = "/home/user/ticket_7384_repo"
JSON_FILE = "/home/user/resolution.json"
EXPECTED_HASH_FILE = "/tmp/expected_hash.txt"

def test_make_test_passes():
    """Verify that 'make test' runs successfully and outputs 'All tests passed!'."""
    # Clean first
    subprocess.run(["make", "clean"], cwd=REPO_DIR, capture_output=True)

    # Run make test
    make_result = subprocess.run(["make", "test"], cwd=REPO_DIR, capture_output=True, text=True)
    assert make_result.returncode == 0, f"'make test' failed to build or run. Stderr: {make_result.stderr}"

    # Run test_runner directly to check output just in case
    test_runner_path = os.path.join(REPO_DIR, "test_runner")
    assert os.path.isfile(test_runner_path), "test_runner executable was not created."

    run_result = subprocess.run([test_runner_path], cwd=REPO_DIR, capture_output=True, text=True)
    assert run_result.returncode == 0, "test_runner exited with a non-zero status."
    assert "All tests passed!" in run_result.stdout, "test_runner did not output 'All tests passed!'."

def test_resolution_json_exists_and_valid():
    """Verify that the resolution.json file exists and has the correct format and content."""
    assert os.path.isfile(JSON_FILE), f"Resolution file {JSON_FILE} is missing."

    with open(JSON_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse JSON in {JSON_FILE}: {e}")

    assert "linker_fix_file" in data, "Missing 'linker_fix_file' key in JSON."
    assert "Makefile" in data["linker_fix_file"], "The linker_fix_file should be 'Makefile'."

    assert "test_status" in data, "Missing 'test_status' key in JSON."
    assert data["test_status"].lower() == "pass", "The test_status should be 'pass'."

    assert "precision_bug_commit" in data, "Missing 'precision_bug_commit' key in JSON."

    assert os.path.isfile(EXPECTED_HASH_FILE), f"Expected hash file {EXPECTED_HASH_FILE} is missing."
    with open(EXPECTED_HASH_FILE, "r") as f:
        expected_hash = f.read().strip()

    actual_hash = data["precision_bug_commit"].strip()
    assert actual_hash == expected_hash, f"Incorrect precision_bug_commit hash. Expected {expected_hash}, got {actual_hash}."

def test_solver_fixes():
    """Verify that the bugs in solver.c have been fixed."""
    solver_path = os.path.join(REPO_DIR, "solver.c")
    assert os.path.isfile(solver_path), "solver.c is missing."

    with open(solver_path, "r") as f:
        content = f.read()

    # Check off-by-one fix
    assert "i <= n" not in content, "The off-by-one bug (i <= n) is still present in solver.c."

    # Check precision fix
    assert "float guess =" not in content, "The precision bug (float guess =) is still present in solver.c."