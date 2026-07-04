# test_final_state.py

import os
import subprocess
import pytest
import glob

def get_actual_bad_commit(repo_path):
    # Find all commits from v1.0.0 to HEAD
    result = subprocess.run(
        ["git", "rev-list", "v1.0.0..HEAD", "--reverse"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True
    )
    commits = result.stdout.strip().splitlines()

    for commit in commits:
        # Checkout commit
        subprocess.run(["git", "checkout", commit], cwd=repo_path, capture_output=True, check=False)
        # Run tests
        test_result = subprocess.run(["go", "test", "./..."], cwd=repo_path, capture_output=True)
        if test_result.returncode != 0:
            # Restore HEAD
            subprocess.run(["git", "checkout", "main"], cwd=repo_path, capture_output=True, check=False)
            return commit

    # Restore HEAD
    subprocess.run(["git", "checkout", "main"], cwd=repo_path, capture_output=True, check=False)
    return None

def test_report_content_and_commit():
    report_path = "/home/user/report.txt"
    assert os.path.exists(report_path), f"Report file missing at {report_path}"

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    assert len(lines) >= 2, f"Report file must contain at least 2 lines, found {len(lines)}"

    reported_commit = lines[0]
    reported_filter = lines[1]

    assert reported_filter == "/home/user/diag_filter", f"Line 2 of report should be '/home/user/diag_filter', got '{reported_filter}'"

    repo_path = "/home/user/diag_service"
    actual_bad_commit = get_actual_bad_commit(repo_path)
    assert actual_bad_commit is not None, "Could not determine the bad commit in /home/user/diag_service"

    # Check if the reported commit is a prefix or exact match
    assert reported_commit == actual_bad_commit or actual_bad_commit.startswith(reported_commit), \
        f"Incorrect bad commit reported. Expected {actual_bad_commit}, got {reported_commit}"

def test_diag_filter_adversarial_corpus():
    filter_bin = "/home/user/diag_filter"
    assert os.path.exists(filter_bin), f"Filter binary missing at {filter_bin}"
    assert os.access(filter_bin, os.X_OK), f"Filter binary at {filter_bin} is not executable"

    clean_corpus_dir = "/app/corpora/clean"
    evil_corpus_dir = "/app/corpora/evil"

    clean_files = glob.glob(os.path.join(clean_corpus_dir, "*"))
    evil_files = glob.glob(os.path.join(evil_corpus_dir, "*"))

    assert len(clean_files) > 0, "No clean corpus files found to test against"
    assert len(evil_files) > 0, "No evil corpus files found to test against"

    clean_failed = []
    for fpath in clean_files:
        res = subprocess.run([filter_bin, fpath], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(fpath))

    evil_bypassed = []
    for fpath in evil_files:
        res = subprocess.run([filter_bin, fpath], capture_output=True)
        if res.returncode == 0:
            evil_bypassed.append(os.path.basename(fpath))

    error_msgs = []
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed[:5])}")
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_bypassed[:5])}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))