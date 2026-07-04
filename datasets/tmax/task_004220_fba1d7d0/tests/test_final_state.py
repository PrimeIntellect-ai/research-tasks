# test_final_state.py

import os
import stat
import subprocess
import tempfile
import shutil
import pytest

def test_fstab_conf_exists_and_correct():
    fstab_path = "/home/user/operator/fstab.conf"
    assert os.path.isfile(fstab_path), f"Missing {fstab_path}"

    with open(fstab_path, "r") as f:
        content = f.read()

    expected_line = "tmpfs /home/user/operator/run tmpfs rw,nodev,nosuid,size=50M 0 0"
    assert expected_line in content, f"{fstab_path} does not contain the required tmpfs line."

def test_run_directory_permissions():
    run_dir = "/home/user/operator/run"
    assert os.path.isdir(run_dir), f"Missing directory {run_dir}"

    st = os.stat(run_dir)
    # Check that group and others have no permissions (mask 0077)
    assert (st.st_mode & 0o077) == 0, f"Permissions for {run_dir} are too open. Group or others have access."

def test_pre_receive_hook_exists_and_executable():
    hook_path = "/home/user/k8s-manifests.git/hooks/pre-receive"
    assert os.path.isfile(hook_path), f"Missing pre-receive hook at {hook_path}"
    assert os.access(hook_path, os.X_OK), f"pre-receive hook at {hook_path} is not executable"

def test_corpus_pushes():
    bare_repo = "/home/user/k8s-manifests.git"
    clean_corpus = "/app/corpus/clean"
    evil_corpus = "/app/corpus/evil"

    assert os.path.isdir(clean_corpus), "Clean corpus directory missing."
    assert os.path.isdir(evil_corpus), "Evil corpus directory missing."

    clean_files = [f for f in os.listdir(clean_corpus) if os.path.isfile(os.path.join(clean_corpus, f))]
    evil_files = [f for f in os.listdir(evil_corpus) if os.path.isfile(os.path.join(evil_corpus, f))]

    assert len(clean_files) > 0, "No files found in clean corpus."
    assert len(evil_files) > 0, "No files found in evil corpus."

    # Setup a temporary clone to test pushes
    with tempfile.TemporaryDirectory() as tmpdir:
        clone_dir = os.path.join(tmpdir, "repo")
        subprocess.run(["git", "clone", bare_repo, clone_dir], check=True, capture_output=True)

        # Configure git user
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=clone_dir, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=clone_dir, check=True)

        # Test clean corpus files
        clean_modified = []
        for cf in clean_files:
            src = os.path.join(clean_corpus, cf)
            dst = os.path.join(clone_dir, cf)
            shutil.copy(src, dst)
            subprocess.run(["git", "add", cf], cwd=clone_dir, check=True)
            subprocess.run(["git", "commit", "-m", f"Add clean file {cf}"], cwd=clone_dir, check=True)

            # Push should succeed
            res = subprocess.run(["git", "push", "origin", "master"], cwd=clone_dir, capture_output=True)
            if res.returncode != 0:
                clean_modified.append(cf)

        # Test evil corpus files
        evil_bypassed = []
        for ef in evil_files:
            src = os.path.join(evil_corpus, ef)
            dst = os.path.join(clone_dir, ef)
            shutil.copy(src, dst)
            subprocess.run(["git", "add", ef], cwd=clone_dir, check=True)
            subprocess.run(["git", "commit", "-m", f"Add evil file {ef}"], cwd=clone_dir, check=True)

            # Push should fail
            res = subprocess.run(["git", "push", "origin", "master"], cwd=clone_dir, capture_output=True)
            if res.returncode == 0:
                evil_bypassed.append(ef)
            else:
                # Reset the commit since it failed to push, so we can test the next one from a clean state
                subprocess.run(["git", "reset", "--hard", "HEAD~1"], cwd=clone_dir, check=True)

        error_msgs = []
        if clean_modified:
            error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")
        if evil_bypassed:
            error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed (accepted): {', '.join(evil_bypassed)}")

        if error_msgs:
            pytest.fail(" | ".join(error_msgs))