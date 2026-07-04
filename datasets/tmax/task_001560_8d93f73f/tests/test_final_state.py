# test_final_state.py

import os
import stat
import subprocess
import pytest
from pathlib import Path

def test_symlink_and_permissions():
    """Check that the www symlink is correct and deploy directory permissions are at least 755."""
    www_path = "/home/user/www"
    deploy_path = "/home/user/deploy"
    current_path = "/home/user/deploy/current"

    assert os.path.islink(www_path), f"{www_path} must be a symlink"
    assert os.readlink(www_path) == current_path, f"{www_path} must point to {current_path}"

    deploy_stat = os.stat(deploy_path)
    mode = deploy_stat.st_mode

    # Check if permissions are at least 755 (owner rwx, group rx, others rx)
    assert bool(mode & stat.S_IRUSR), "Owner must have read permission on deploy dir"
    assert bool(mode & stat.S_IWUSR), "Owner must have write permission on deploy dir"
    assert bool(mode & stat.S_IXUSR), "Owner must have execute permission on deploy dir"
    assert bool(mode & stat.S_IRGRP), "Group must have read permission on deploy dir"
    assert bool(mode & stat.S_IXGRP), "Group must have execute permission on deploy dir"
    assert bool(mode & stat.S_IROTH), "Others must have read permission on deploy dir"
    assert bool(mode & stat.S_IXOTH), "Others must have execute permission on deploy dir"

def test_git_hooks():
    """Check that the Git hooks are implemented and contain expected logic."""
    pre_receive = "/home/user/site.git/hooks/pre-receive"
    post_receive = "/home/user/site.git/hooks/post-receive"

    assert os.path.isfile(pre_receive), f"pre-receive hook missing at {pre_receive}"
    assert os.access(pre_receive, os.X_OK), f"pre-receive hook at {pre_receive} is not executable"
    with open(pre_receive, "r") as f:
        pre_content = f.read()
    assert "filter.sh" in pre_content, "pre-receive hook does not appear to call filter.sh"

    assert os.path.isfile(post_receive), f"post-receive hook missing at {post_receive}"
    assert os.access(post_receive, os.X_OK), f"post-receive hook at {post_receive} is not executable"
    with open(post_receive, "r") as f:
        post_content = f.read()
    assert "checkout" in post_content and "/home/user/deploy/current" in post_content, "post-receive hook does not appear to checkout to the deploy directory"

def test_filter_sh_adversarial_corpus():
    """Test the filter.sh script against the adversarial corpus."""
    filter_script = "/home/user/filter.sh"
    assert os.path.isfile(filter_script), f"Filter script missing at {filter_script}"
    assert os.access(filter_script, os.X_OK), f"Filter script at {filter_script} is not executable"

    clean_dir = Path("/app/corpus/clean")
    evil_dir = Path("/app/corpus/evil")

    clean_files = list(clean_dir.iterdir()) if clean_dir.exists() else []
    evil_files = list(evil_dir.iterdir()) if evil_dir.exists() else []

    assert clean_files, f"No clean corpus files found in {clean_dir}"
    assert evil_files, f"No evil corpus files found in {evil_dir}"

    bypassed_evil = []
    modified_clean = []

    # Test evil corpus (expected exit code 1)
    for evil_file in evil_files:
        if evil_file.is_file():
            result = subprocess.run([filter_script, str(evil_file)], capture_output=True)
            if result.returncode != 1:
                bypassed_evil.append(evil_file.name)

    # Test clean corpus (expected exit code 0)
    for clean_file in clean_files:
        if clean_file.is_file():
            result = subprocess.run([filter_script, str(clean_file)], capture_output=True)
            if result.returncode != 0:
                modified_clean.append(clean_file.name)

    error_messages = []
    if bypassed_evil:
        error_messages.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        error_messages.append(f"{len(modified_clean)} of {len(clean_files)} clean modified (rejected): {', '.join(modified_clean)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))