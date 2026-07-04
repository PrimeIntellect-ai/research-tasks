# test_final_state.py

import os
import subprocess
import pytest

def test_vm_user_sync_installed_and_lint_passes():
    venv_bin = "/home/user/venv/bin/vm-user-sync"
    assert os.path.isfile(venv_bin), f"Executable {venv_bin} is missing."
    assert os.access(venv_bin, os.X_OK), f"Executable {venv_bin} is not executable."

    result = subprocess.run([venv_bin, "--lint-templates"], capture_output=True, text=True)
    assert result.returncode == 0, f"vm-user-sync lint failed. Output: {result.stdout} {result.stderr}"

def test_git_repo_and_hook():
    repo_path = "/home/user/provisioning.git"
    assert os.path.isdir(repo_path), f"Git repo {repo_path} is missing."

    result = subprocess.run(["git", "-C", repo_path, "rev-parse", "--is-bare-repository"], capture_output=True, text=True)
    assert result.returncode == 0 and result.stdout.strip() == "true", f"Repository at {repo_path} is not a bare Git repository."

    hook_path = os.path.join(repo_path, "hooks", "pre-receive")
    assert os.path.isfile(hook_path), f"Hook {hook_path} is missing."
    assert os.access(hook_path, os.X_OK), f"Hook {hook_path} is not executable."

    with open(hook_path, "r") as f:
        content = f.read()
    assert "# VALIDATOR_INTEGRATION_READY" in content, f"Hook {hook_path} is missing the placeholder comment."

def test_validator_against_corpus():
    validator_script = "/home/user/validator.py"
    assert os.path.isfile(validator_script), f"Validator script {validator_script} is missing."

    clean_base = "/app/corpus/clean"
    evil_base = "/app/corpus/evil"

    clean_dirs = [os.path.join(clean_base, d) for d in os.listdir(clean_base) if os.path.isdir(os.path.join(clean_base, d))]
    evil_dirs = [os.path.join(evil_base, d) for d in os.listdir(evil_base) if os.path.isdir(os.path.join(evil_base, d))]

    clean_failed = []
    for d in clean_dirs:
        res = subprocess.run(["python3", validator_script, d], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(d))

    evil_failed = []
    for d in evil_dirs:
        res = subprocess.run(["python3", validator_script, d], capture_output=True)
        if res.returncode != 1:
            evil_failed.append(os.path.basename(d))

    errors = []
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_dirs)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_dirs)} clean modified/rejected: {', '.join(clean_failed)}")

    assert not errors, "Validator corpus test failed: " + "; ".join(errors)