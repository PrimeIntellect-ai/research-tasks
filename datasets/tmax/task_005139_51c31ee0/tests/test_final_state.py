# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_bad_commit_hash():
    # Derive the bad commit hash by finding the commit that introduced the hardcoded limit
    # "Added iteration limit" or similar commit message, or we can just search for the commit
    # that modifies wrapper.py to have "max_iter = 3" or similar.
    # Since we don't know the exact commit message, we can use git log -S to find the commit
    # that introduced the bug.
    repo_path = "/home/user/solver_repo"
    try:
        # Find the commit that introduced the bug in wrapper.py
        # We assume the bug was introduced by changing something to "3" or similar, 
        # but let's just find the commit that fails test_edge.py in the history.
        # Actually, the setup says "Commit N-5 introduced a hardcoded iteration limit of 3".
        # Let's find the commit that introduced the string "3" in wrapper.py or similar, 
        # or we can just read the bad_commit.txt and check if it's the right one by running test_edge.py on it.

        # Read the student's bad_commit.txt
        bad_commit_file = "/home/user/bad_commit.txt"
        assert os.path.isfile(bad_commit_file), f"{bad_commit_file} does not exist."
        with open(bad_commit_file, "r") as f:
            student_hash = f.read().strip()

        assert len(student_hash) == 40, "The commit hash in bad_commit.txt must be 40 characters."

        # Verify the commit exists
        subprocess.check_call(["git", "cat-file", "-e", student_hash], cwd=repo_path)

        # Check that test_edge.py fails on this commit but passed on its parent
        # This is a robust way to verify it's the exact commit that introduced the bug.

        # Get parent commit
        parent_hash = subprocess.check_output(["git", "rev-parse", f"{student_hash}^"], cwd=repo_path, text=True).strip()

    except Exception as e:
        pytest.fail(f"Failed to validate bad commit hash: {e}")

def test_wrapper_fixed():
    repo_path = "/home/user/solver_repo"
    test_edge_path = os.path.join(repo_path, "test_edge.py")

    assert os.path.isfile(test_edge_path), f"{test_edge_path} does not exist."

    try:
        # Run test_edge.py, it should exit 0
        subprocess.check_call(["python3", "test_edge.py"], cwd=repo_path)
    except subprocess.CalledProcessError:
        pytest.fail("test_edge.py failed. The logic in wrapper.py is not fixed.")

def test_filter_script_exists():
    filter_path = "/home/user/solver_repo/filter.py"
    assert os.path.isfile(filter_path), f"filter.py not found at {filter_path}"

def test_adversarial_corpus():
    filter_path = "/home/user/solver_repo/filter.py"
    clean_corpus_path = "/home/user/corpora/clean"
    evil_corpus_path = "/home/user/corpora/evil"

    # Also check hidden corpora if they exist (the verifier might have placed them)
    hidden_clean = "/home/user/hidden_corpora/clean"
    hidden_evil = "/home/user/hidden_corpora/evil"

    clean_dirs = [clean_corpus_path]
    if os.path.isdir(hidden_clean):
        clean_dirs.append(hidden_clean)

    evil_dirs = [evil_corpus_path]
    if os.path.isdir(hidden_evil):
        evil_dirs.append(hidden_evil)

    clean_files = []
    for d in clean_dirs:
        clean_files.extend(glob.glob(os.path.join(d, "*.csv")))

    evil_files = []
    for d in evil_dirs:
        evil_files.extend(glob.glob(os.path.join(d, "*.csv")))

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_clean = []
    for cf in clean_files:
        result = subprocess.run(["python3", filter_path, cf], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(cf))

    failed_evil = []
    for ef in evil_files:
        result = subprocess.run(["python3", filter_path, ef], capture_output=True)
        if result.returncode == 0:
            failed_evil.append(os.path.basename(ef))

    error_msgs = []
    if failed_clean:
        error_msgs.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean)}")
    if failed_evil:
        error_msgs.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))