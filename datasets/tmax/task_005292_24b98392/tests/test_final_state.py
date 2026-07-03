# test_final_state.py

import os
import subprocess
import pytest

def test_crash_frame_recovered():
    crash_frame_path = "/home/user/crash_frame.txt"
    assert os.path.isfile(crash_frame_path), f"Missing {crash_frame_path}"

    with open(crash_frame_path, "r") as f:
        content = f.read().strip()

    assert content == "845", f"Expected crash frame to be '845', but got '{content}'"

def test_sanitizer_executable():
    sanitizer_path = "/home/user/sanitizer.sh"
    assert os.path.isfile(sanitizer_path), f"Missing {sanitizer_path}"
    assert os.access(sanitizer_path, os.X_OK), f"Script {sanitizer_path} is not executable"

def test_sanitizer_adversarial_corpus():
    sanitizer_path = "/home/user/sanitizer.sh"
    evil_dir = "/home/user/metadata/evil/"
    clean_dir = "/home/user/metadata/clean/"

    assert os.path.isdir(evil_dir), f"Missing evil corpus directory: {evil_dir}"
    assert os.path.isdir(clean_dir), f"Missing clean corpus directory: {clean_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    assert len(evil_files) > 0, "Evil corpus is empty"
    assert len(clean_files) > 0, "Clean corpus is empty"

    evil_bypassed = []
    clean_modified_or_failed = []

    for evil_file in evil_files:
        with open(evil_file, "rb") as f:
            payload = f.read()

        result = subprocess.run([sanitizer_path], input=payload, capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append((os.path.basename(evil_file), result.returncode))

    for clean_file in clean_files:
        with open(clean_file, "rb") as f:
            payload = f.read()

        result = subprocess.run([sanitizer_path], input=payload, capture_output=True)
        if result.returncode != 0 or result.stdout != payload:
            clean_modified_or_failed.append((os.path.basename(clean_file), result.returncode))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {evil_bypassed[:5]}")
    if clean_modified_or_failed:
        error_msgs.append(f"{len(clean_modified_or_failed)} of {len(clean_files)} clean modified or failed: {clean_modified_or_failed[:5]}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))