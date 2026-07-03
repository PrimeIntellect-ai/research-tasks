# test_final_state.py

import os
import pytest

def test_validator_source_exists():
    """Verify that the validator source code exists."""
    source_path = "/home/user/validator.cpp"
    assert os.path.isfile(source_path), f"Missing validator source file: {source_path}"

def test_validator_binary_exists():
    """Verify that the compiled validator binary exists and is executable."""
    binary_path = "/home/user/validator"
    assert os.path.isfile(binary_path), f"Missing compiled validator binary: {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Validator binary is not executable: {binary_path}"

def test_deploy_log_content():
    """Verify that the deploy.log file exists and contains the correct decision."""
    log_path = "/home/user/deploy.log"
    assert os.path.isfile(log_path), f"Missing deploy.log file: {log_path}"

    with open(log_path, 'r') as f:
        content = f.read().strip()

    assert content == "DEPLOY_APPROVED", f"Expected DEPLOY_APPROVED in deploy.log, but got: '{content}'"