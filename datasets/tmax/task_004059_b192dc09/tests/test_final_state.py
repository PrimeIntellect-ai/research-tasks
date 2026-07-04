# test_final_state.py
import os
import subprocess
import pytest

def test_bad_commit_identified():
    repo_path = "/home/user/pipeline"
    bad_commit_file = "/home/user/bad_commit.txt"

    assert os.path.isfile(bad_commit_file), f"File {bad_commit_file} not found"

    with open(bad_commit_file, "r") as f:
        student_commit = f.read().strip()

    result = subprocess.run(
        ["git", "-C", repo_path, "rev-parse", "HEAD~63"], 
        capture_output=True, text=True, check=True
    )
    expected_commit = result.stdout.strip()

    assert student_commit == expected_commit, f"Expected bad commit {expected_commit}, but got {student_commit}"

def test_filter_script_adversarial_corpus():
    filter_script = "/home/user/filter.sh"
    assert os.path.isfile(filter_script), f"Filter script {filter_script} not found"

    evil_dir = "/app/corpus/evil"
    clean_dir = "/app/corpus/clean"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    assert len(evil_files) > 0, "No evil files found in corpus"
    assert len(clean_files) > 0, "No clean files found in corpus"

    evil_bypassed = []
    for ef in evil_files:
        result = subprocess.run(["bash", filter_script, ef], capture_output=True)
        if result.returncode != 1 or len(result.stdout) > 0:
            evil_bypassed.append(os.path.basename(ef))

    clean_modified = []
    for cf in clean_files:
        with open(cf, "rb") as f:
            expected_content = f.read()
        result = subprocess.run(["bash", filter_script, cf], capture_output=True)
        if result.returncode != 0 or result.stdout != expected_content:
            clean_modified.append(os.path.basename(cf))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not error_msgs, " | ".join(error_msgs)