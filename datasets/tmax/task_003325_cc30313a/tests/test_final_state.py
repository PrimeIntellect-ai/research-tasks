# test_final_state.py

import os
import subprocess
import pytest

def get_actual_bad_commit():
    repo = "/home/user/pipeline"
    cmd = ["git", "-C", repo, "log", "-S", "$((", "--format=%H", "--reverse"]
    try:
        out = subprocess.check_output(cmd, text=True).strip().split('\n')
        return out[0] if out[0] else None
    except subprocess.CalledProcessError:
        return None

def test_bad_commit_logged():
    log_path = "/home/user/bad_commit.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    with open(log_path, "r") as f:
        student_commit = f.read().strip()

    actual_commit = get_actual_bad_commit()
    assert actual_commit is not None, "Could not determine the actual bad commit from the repository."
    assert student_commit == actual_commit, f"Expected bad commit {actual_commit}, but got {student_commit}."

def test_video_analysis_log():
    log_path = "/home/user/video_analysis.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read()

    expected_val = "9223372036854775809"
    assert expected_val in content, f"Expected final cumulative intensity diff {expected_val} not found in {log_path}."
    assert "-9223372036854775807" not in content, "Found overflowed negative value in the analysis log."

def test_adversarial_sanitizer():
    sanitizer_script = "/home/user/sanitizer.sh"
    assert os.path.isfile(sanitizer_script), f"Sanitizer script {sanitizer_script} is missing."

    evil_corpus_path = "/home/user/corpora/evil/"
    clean_corpus_path = "/home/user/corpora/clean/"

    evil_files = [os.path.join(evil_corpus_path, f) for f in os.listdir(evil_corpus_path) if os.path.isfile(os.path.join(evil_corpus_path, f))]
    clean_files = [os.path.join(clean_corpus_path, f) for f in os.listdir(clean_corpus_path) if os.path.isfile(os.path.join(clean_corpus_path, f))]

    evil_bypassed = []
    clean_modified = []

    for fpath in evil_files:
        res = subprocess.run(["bash", sanitizer_script, fpath], capture_output=True)
        if res.returncode != 1:
            evil_bypassed.append(os.path.basename(fpath))

    for fpath in clean_files:
        res = subprocess.run(["bash", sanitizer_script, fpath], capture_output=True)
        if res.returncode != 0:
            clean_modified.append(os.path.basename(fpath))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))