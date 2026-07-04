# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_uroute_compiled():
    """Verify that the legacy C routing tool has been compiled successfully."""
    cli_path = "/app/vendored/uroute-0.5.1/uroute_cli"
    assert os.path.isfile(cli_path), f"Expected compiled executable at {cli_path} is missing."
    assert os.access(cli_path, os.X_OK), f"Executable {cli_path} is not executable."

def test_uroute_cli_behavior():
    """Check that uroute_cli behaves correctly for valid and invalid routes."""
    cli_path = "/app/vendored/uroute-0.5.1/uroute_cli"

    # Valid route
    res = subprocess.run([cli_path, "/api/v1/users"], capture_output=True)
    assert res.returncode == 0, f"uroute_cli failed on valid route /api/v1/users. Exit code: {res.returncode}"

    # Invalid route
    res = subprocess.run([cli_path, "/api/v1/admin"], capture_output=True)
    assert res.returncode != 0, f"uroute_cli incorrectly accepted invalid route /api/v1/admin. Exit code: {res.returncode}"

def test_gateway_filter_exists():
    """Ensure the gateway filter Python script exists."""
    script_path = "/home/user/gateway_filter.py"
    assert os.path.isfile(script_path), f"Python script {script_path} is missing."

def test_gateway_filter_against_corpora():
    """Test the gateway filter script against the clean and evil corpora."""
    script_path = "/home/user/gateway_filter.py"

    clean_dir = "/app/corpora/clean_requests"
    evil_dir = "/app/corpora/evil_requests"

    clean_files = glob.glob(os.path.join(clean_dir, "*.txt"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.txt"))

    assert len(clean_files) > 0, "No clean request files found."
    assert len(evil_files) > 0, "No evil request files found."

    clean_failures = []
    for cf in clean_files:
        with open(cf, 'r') as f:
            url = f.read().strip()
        res = subprocess.run(["python3", script_path, url], capture_output=True, text=True)
        output = res.stdout.strip()
        if output != "ACCEPT":
            clean_failures.append(os.path.basename(cf))

    evil_failures = []
    for ef in evil_files:
        with open(ef, 'r') as f:
            url = f.read().strip()
        res = subprocess.run(["python3", script_path, url], capture_output=True, text=True)
        output = res.stdout.strip()
        if output != "REJECT":
            evil_failures.append(os.path.basename(ef))

    error_msgs = []
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failures)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))