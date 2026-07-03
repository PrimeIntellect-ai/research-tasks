# test_final_state.py

import os
import subprocess
import glob
import tempfile
import shutil
import pytest

QUOTA_CHECKER_PATH = "/home/user/quota_checker"
CLEAN_DIR = "/app/corpora/clean"
EVIL_DIR = "/app/corpora/evil"
GIT_REPO_URL = "http://localhost:8080/allocations.git"
GIT_REPO_LOCAL = "/home/user/allocations.git"

def test_quota_checker_exists_and_executable():
    assert os.path.isfile(QUOTA_CHECKER_PATH), f"Quota checker binary not found at {QUOTA_CHECKER_PATH}"
    assert os.access(QUOTA_CHECKER_PATH, os.X_OK), f"Quota checker at {QUOTA_CHECKER_PATH} is not executable"

def test_quota_checker_clean_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_DIR, "*.alloc"))
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_files = []
    for f in clean_files:
        result = subprocess.run([QUOTA_CHECKER_PATH, f], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(f))

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean files rejected: {', '.join(failed_files)}"

def test_quota_checker_evil_corpus():
    evil_files = glob.glob(os.path.join(EVIL_DIR, "*.alloc"))
    assert len(evil_files) > 0, "No evil corpus files found."

    bypassed_files = []
    for f in evil_files:
        result = subprocess.run([QUOTA_CHECKER_PATH, f], capture_output=True)
        if result.returncode == 0:
            bypassed_files.append(os.path.basename(f))

    assert not bypassed_files, f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed: {', '.join(bypassed_files)}"

def test_git_repo_exists():
    assert os.path.isdir(GIT_REPO_LOCAL), f"Git repo not found at {GIT_REPO_LOCAL}"
    assert os.path.isfile(os.path.join(GIT_REPO_LOCAL, "config")), "Git repo does not appear to be initialized"

def test_git_pre_receive_hook_exists():
    hook_path = os.path.join(GIT_REPO_LOCAL, "hooks", "pre-receive")
    assert os.path.isfile(hook_path), f"pre-receive hook missing at {hook_path}"
    assert os.access(hook_path, os.X_OK), "pre-receive hook is not executable"

def test_nginx_git_http_push():
    # Attempt to clone, commit, and push over HTTP
    with tempfile.TemporaryDirectory() as tmpdir:
        clone_dir = os.path.join(tmpdir, "allocations")

        # Clone
        res = subprocess.run(["git", "clone", GIT_REPO_URL, clone_dir], capture_output=True)
        assert res.returncode == 0, f"Failed to clone over HTTP: {res.stderr.decode()}"

        # We need a valid user from acl.txt to make a valid alloc
        acl_path = "/app/acl.txt"
        valid_user = "admin"
        if os.path.isfile(acl_path):
            with open(acl_path, "r") as f:
                lines = f.read().splitlines()
                if lines:
                    valid_user = lines[0]

        # Create a valid alloc
        valid_alloc = os.path.join(clone_dir, "test_valid.alloc")
        with open(valid_alloc, "w") as f:
            f.write(f"USER: {valid_user}\nMOUNT: /mnt/storage/test\nSIZE: 10\n")

        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=clone_dir, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=clone_dir, check=True)

        subprocess.run(["git", "add", "test_valid.alloc"], cwd=clone_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Add valid alloc"], cwd=clone_dir, check=True)

        # Push valid
        res = subprocess.run(["git", "push", "origin", "master"], cwd=clone_dir, capture_output=True)
        assert res.returncode == 0, f"Failed to push valid commit over HTTP: {res.stderr.decode()}"

        # Create an invalid alloc
        invalid_alloc = os.path.join(clone_dir, "test_invalid.alloc")
        with open(invalid_alloc, "w") as f:
            f.write(f"USER: {valid_user}\nMOUNT: /mnt/storage/test\nSIZE: 999\n")

        subprocess.run(["git", "add", "test_invalid.alloc"], cwd=clone_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Add invalid alloc"], cwd=clone_dir, check=True)

        # Push invalid (should be rejected by pre-receive hook)
        res = subprocess.run(["git", "push", "origin", "master"], cwd=clone_dir, capture_output=True)
        assert res.returncode != 0, "Pushing an invalid alloc file succeeded, but it should have been rejected by the pre-receive hook."