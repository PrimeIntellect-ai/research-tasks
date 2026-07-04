# test_final_state.py

import os
import subprocess
import pytest

VALIDATOR_SCRIPT = "/home/user/validate_config.py"
CLEAN_DIR = "/app/clean"
EVIL_DIR = "/app/evil"
GIT_DIR = "/home/user/provisioning.git"
HOOK_PATH = os.path.join(GIT_DIR, "hooks/pre-receive")

def test_validator_script_exists_and_executable():
    assert os.path.isfile(VALIDATOR_SCRIPT), f"Validator script missing at {VALIDATOR_SCRIPT}"
    assert os.access(VALIDATOR_SCRIPT, os.X_OK) or VALIDATOR_SCRIPT.endswith('.py'), f"Validator script {VALIDATOR_SCRIPT} is not executable."

def test_clean_corpus_accepted():
    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    assert len(clean_files) > 0, f"No files found in clean corpus {CLEAN_DIR}"

    failed_files = []
    for fpath in clean_files:
        result = subprocess.run(
            ["python3", VALIDATOR_SCRIPT, fpath],
            capture_output=True
        )
        if result.returncode != 0:
            failed_files.append(os.path.basename(fpath))

    total = len(clean_files)
    failed_count = len(failed_files)
    assert failed_count == 0, f"{failed_count} of {total} clean modified (rejected). Offending files: {', '.join(failed_files)}"

def test_evil_corpus_rejected():
    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    assert len(evil_files) > 0, f"No files found in evil corpus {EVIL_DIR}"

    bypassed_files = []
    for fpath in evil_files:
        result = subprocess.run(
            ["python3", VALIDATOR_SCRIPT, fpath],
            capture_output=True
        )
        if result.returncode == 0:
            bypassed_files.append(os.path.basename(fpath))

    total = len(evil_files)
    bypassed_count = len(bypassed_files)
    assert bypassed_count == 0, f"{bypassed_count} of {total} evil bypassed (accepted). Offending files: {', '.join(bypassed_files)}"

def test_git_bare_repo_exists():
    assert os.path.isdir(GIT_DIR), f"Git repository directory missing at {GIT_DIR}"
    config_path = os.path.join(GIT_DIR, "config")
    assert os.path.isfile(config_path), f"Git config missing at {config_path}, is it a bare repo?"

    with open(config_path, "r") as f:
        content = f.read()
        assert "bare = true" in content.lower(), f"Repository at {GIT_DIR} is not a bare repository."

def test_git_hook_exists_and_configured():
    assert os.path.isfile(HOOK_PATH), f"Git pre-receive hook missing at {HOOK_PATH}"
    assert os.access(HOOK_PATH, os.X_OK), f"Git pre-receive hook at {HOOK_PATH} is not executable."

    with open(HOOK_PATH, "r") as f:
        content = f.read()
        assert "STRICT_MODE=1" in content, f"pre-receive hook does not export STRICT_MODE=1"
        assert "validate_config.py" in content, f"pre-receive hook does not call validate_config.py"