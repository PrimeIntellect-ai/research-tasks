# test_final_state.py

import os
import subprocess
import pytest

def test_part1_breach_frame():
    frame_file = "/home/user/breach_frame.txt"
    assert os.path.isfile(frame_file), f"Missing breach frame file at {frame_file}"

    with open(frame_file, "r") as f:
        content = f.read().strip()

    assert content == "145", f"Expected breach frame to be '145', but got '{content}'"

def test_part2_detect_tunnels():
    script_path = "/home/user/detect_tunnels.py"
    assert os.path.isfile(script_path), f"Missing detect_tunnels.py script at {script_path}"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"Missing clean corpus directory at {clean_dir}"
    assert os.path.isdir(evil_dir), f"Missing evil corpus directory at {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failures = []
    for cf in clean_files:
        result = subprocess.run(["python3", script_path, cf], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(cf))

    evil_failures = []
    for ef in evil_files:
        result = subprocess.run(["python3", script_path, ef], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(os.path.basename(ef))

    error_messages = []
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean files failed (expected exit code 0): {', '.join(clean_failures)}")
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil files bypassed (expected exit code 1): {', '.join(evil_failures)}")

    assert not error_messages, " | ".join(error_messages)