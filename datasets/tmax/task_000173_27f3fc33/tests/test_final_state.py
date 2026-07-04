# test_final_state.py

import os
import subprocess
import json
import pytest

def test_vmm_deploy_installed_and_working():
    binary_path = "/home/user/.local/bin/vmm-deploy"
    assert os.path.isfile(binary_path), f"The binary {binary_path} was not installed."
    assert os.access(binary_path, os.X_OK), f"The binary {binary_path} is not executable."

    result = subprocess.run([binary_path, "--version"], capture_output=True, text=True)
    assert result.returncode == 0, f"vmm-deploy failed with exit code {result.returncode}. Stderr: {result.stderr}"
    assert "vmm-deploy 0.5.0" in result.stdout, f"vmm-deploy output did not contain 'vmm-deploy 0.5.0'. Output: {result.stdout}"

def test_validator_adversarial_corpus():
    validator_path = "/home/user/validator.py"
    assert os.path.isfile(validator_path), f"Validator script {validator_path} does not exist."

    evil_dir = "/tests/corpus/evil"
    clean_dir = "/tests/corpus/clean"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith(".json")]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith(".json")]

    assert len(evil_files) > 0, "No evil corpus files found."
    assert len(clean_files) > 0, "No clean corpus files found."

    evil_bypassed = []
    for evil_file in evil_files:
        result = subprocess.run(["python3", validator_path, evil_file], capture_output=True, text=True)
        if result.returncode != 1 or result.stdout.strip() != "EVIL":
            evil_bypassed.append(os.path.basename(evil_file))

    clean_modified = []
    for clean_file in clean_files:
        result = subprocess.run(["python3", validator_path, clean_file], capture_output=True, text=True)
        if result.returncode != 0 or result.stdout.strip() != "CLEAN":
            clean_modified.append(os.path.basename(clean_file))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_modified)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))