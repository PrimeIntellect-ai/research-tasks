# test_final_state.py

import os
import subprocess
import re
import pytest

HOME_DIR = "/home/user"
NETWORK_ENV = os.path.join(HOME_DIR, "network_env.sh")
FORWARDER = os.path.join(HOME_DIR, "forwarder.py")
CHECK_QUOTA = os.path.join(HOME_DIR, "check_quota.py")
RUN_TEST = os.path.join(HOME_DIR, "run_test.sh")
LOG_DIR = os.path.join(HOME_DIR, "logs")
FORWARDER_LOG = os.path.join(LOG_DIR, "forwarder.log")
QUOTA_STATUS = os.path.join(HOME_DIR, "quota_status.txt")

def test_files_exist_and_executable():
    """Ensure all required scripts are created and executable."""
    required_files = [NETWORK_ENV, FORWARDER, CHECK_QUOTA, RUN_TEST]
    for f in required_files:
        assert os.path.isfile(f), f"Required file {f} does not exist."
        assert os.access(f, os.X_OK), f"File {f} is not executable."

def test_network_env_vars():
    """Ensure network_env.sh exports the correct variables."""
    cmd = f"source {NETWORK_ENV} && env"
    result = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to source {NETWORK_ENV}"

    env_output = result.stdout
    assert "FWD_LISTEN_PORT=8080" in env_output, "FWD_LISTEN_PORT not correctly exported."
    assert "FWD_TARGET_PORT=9090" in env_output, "FWD_TARGET_PORT not correctly exported."
    assert f"LOG_DIR={LOG_DIR}" in env_output, "LOG_DIR not correctly exported."

def test_forwarder_script_contents():
    """Ensure forwarder.py contains the correct RotatingFileHandler setup."""
    with open(FORWARDER, "r") as f:
        content = f.read()

    assert "RotatingFileHandler" in content, "forwarder.py does not use RotatingFileHandler."

    # Check maxBytes=512
    assert re.search(r"maxBytes\s*=\s*512", content), "forwarder.py does not set maxBytes=512."
    # Check backupCount=2
    assert re.search(r"backupCount\s*=\s*2", content), "forwarder.py does not set backupCount=2."

def test_run_test_sh_execution():
    """Execute run_test.sh and verify it runs successfully."""
    # Run the integration script to generate logs and quota status
    result = subprocess.run(["bash", RUN_TEST], capture_output=True, text=True)
    assert result.returncode == 0, f"run_test.sh failed to execute properly. Stderr: {result.stderr}"

def test_logs_created_and_populated():
    """Ensure the log file is created and contains the expected log message."""
    assert os.path.isdir(LOG_DIR), f"Log directory {LOG_DIR} was not created."
    assert os.path.isfile(FORWARDER_LOG), f"Log file {FORWARDER_LOG} was not created."

    with open(FORWARDER_LOG, "r") as f:
        log_content = f.read()

    assert "New connection established" in log_content, "The expected log message 'New connection established' was not found in the forwarder log."

def test_quota_status():
    """Ensure the quota status file is created and contains the correct initial state."""
    assert os.path.isfile(QUOTA_STATUS), f"Quota status file {QUOTA_STATUS} was not created."

    with open(QUOTA_STATUS, "r") as f:
        status = f.read().strip()

    assert status == "QUOTA_OK", f"Expected quota status 'QUOTA_OK', but found '{status}'."