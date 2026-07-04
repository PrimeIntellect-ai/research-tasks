# test_final_state.py
import os
import time
import subprocess
import pytest

def test_auditor_bin_exists():
    """Verify that the compiled binary is placed at the correct path."""
    bin_path = "/home/user/auditor_bin"
    assert os.path.isfile(bin_path), f"The executable {bin_path} is missing. Did you compile and copy it?"
    assert os.access(bin_path, os.X_OK), f"The file {bin_path} is not executable."

def test_cargo_test_passes():
    """Verify that the unit tests for URL decoding pass."""
    manifest_path = "/app/route-auth-auditor/Cargo.toml"
    assert os.path.isfile(manifest_path), f"Cargo.toml missing at {manifest_path}"

    test_res = subprocess.run(
        ["cargo", "test", "--manifest-path", manifest_path],
        capture_output=True,
        text=True
    )
    assert test_res.returncode == 0, f"Unit tests failed. Cargo test output:\n{test_res.stdout}\n{test_res.stderr}"

def test_execution_time_and_correctness():
    """Verify that the binary executes quickly (memoized) and returns the correct result."""
    bin_path = "/home/user/auditor_bin"
    fixture_path = "/app/test_data/large_gateway.json"

    assert os.path.isfile(fixture_path), f"Test fixture missing at {fixture_path}"

    start = time.time()
    res = subprocess.run([bin_path, fixture_path], capture_output=True, text=True)
    elapsed = time.time() - start

    assert res.returncode == 0, f"Binary failed to execute. stderr:\n{res.stderr}"

    # Check execution time threshold
    assert elapsed <= 0.25, f"Execution time {elapsed:.4f}s exceeded threshold of 0.25s. The graph traversal is likely still exponential (unmemoized)."

    # Check correctness of the evaluation
    assert "Root auth evaluated to: true" in res.stdout, f"Binary did not produce the expected output. stdout:\n{res.stdout}"