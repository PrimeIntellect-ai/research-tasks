# test_final_state.py

import os
import subprocess
import pytest

def test_api_key_extracted():
    api_key_path = "/home/user/api_key.txt"
    assert os.path.isfile(api_key_path), f"Missing API key file at {api_key_path}"
    with open(api_key_path, "r") as f:
        content = f.read().strip()
    assert content == "7f8b9c2a1d3e4f5a6b7c8d9e0f1a2b3c", f"Incorrect API key extracted. Found: {content}"

def test_detect_anomaly_script_exists():
    script_path = "/home/user/detect_anomaly.py"
    assert os.path.isfile(script_path), f"Missing anomaly detection script at {script_path}"

def test_adversarial_corpus():
    script_path = "/home/user/detect_anomaly.py"
    clean_dir = "/app/clean"
    evil_dir = "/app/evil"

    assert os.path.isdir(clean_dir), f"Missing clean corpus dir: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Missing evil corpus dir: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    assert clean_files, "Clean corpus is empty."
    assert evil_files, "Evil corpus is empty."

    clean_failed = []
    evil_failed = []

    for cf in clean_files:
        res = subprocess.run(["python3", script_path, cf], capture_output=True, text=True)
        if res.returncode != 0 or "CLEAN" not in res.stdout:
            clean_failed.append(os.path.basename(cf))

    for ef in evil_files:
        res = subprocess.run(["python3", script_path, ef], capture_output=True, text=True)
        if res.returncode != 1 or "EVIL" not in res.stdout:
            evil_failed.append(os.path.basename(ef))

    error_msgs = []
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))