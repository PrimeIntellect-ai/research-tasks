# test_final_state.py

import os
import subprocess
import pytest
from pathlib import Path

def test_router_script_fixed():
    """
    Test that the vendored router.sh script respects the ROUTER_CONFIG_PATH 
    environment variable and exits with 0 on --health-check.
    """
    vendor_script = "/app/vendor/bash-router-1.2.0/router.sh"
    assert os.path.isfile(vendor_script), f"Vendor script {vendor_script} is missing."

    test_conf_dir = "/tmp/test_conf_pytest"
    os.makedirs(test_conf_dir, exist_ok=True)

    env = os.environ.copy()
    env["ROUTER_CONFIG_PATH"] = test_conf_dir

    result = subprocess.run(
        [vendor_script, "--health-check"],
        env=env,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, (
        f"router.sh failed to start with custom ROUTER_CONFIG_PATH. "
        f"Exit code: {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"
    )

def test_api_validator_exists():
    """
    Test that the api_validator.sh script exists and is executable.
    """
    validator_script = "/home/user/api_validator.sh"
    assert os.path.isfile(validator_script), f"Validator script {validator_script} is missing."
    assert os.access(validator_script, os.X_OK), f"Validator script {validator_script} is not executable."

def test_api_validator_adversarial_corpus():
    """
    Test that the api_validator.sh script accepts all clean payloads and rejects all evil payloads.
    """
    validator_script = "/home/user/api_validator.sh"
    clean_dir = Path("/home/user/corpora/clean")
    evil_dir = Path("/home/user/corpora/evil")

    assert clean_dir.is_dir(), f"Clean corpus directory {clean_dir} is missing."
    assert evil_dir.is_dir(), f"Evil corpus directory {evil_dir} is missing."

    clean_files = list(clean_dir.glob("*.json"))
    evil_files = list(evil_dir.glob("*.json"))

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failures = []
    for clean_file in clean_files:
        result = subprocess.run([validator_script, str(clean_file)], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(clean_file.name)

    evil_failures = []
    for evil_file in evil_files:
        result = subprocess.run([validator_script, str(evil_file)], capture_output=True)
        if result.returncode == 0:
            evil_failures.append(evil_file.name)

    error_msgs = []
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failures)}")

    if error_msgs:
        pytest.fail("Adversarial corpus validation failed: " + "; ".join(error_msgs))