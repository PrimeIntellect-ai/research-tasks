# test_final_state.py
import os
import glob
import subprocess
import pytest

def get_executable():
    candidates = [
        "/home/user/filter_payload.py",
        "/home/user/filter_payload.js",
        "/home/user/filter_payload.sh"
    ]
    for c in candidates:
        if os.path.isfile(c):
            if c.endswith(".py"):
                return ["python3", c]
            elif c.endswith(".js"):
                return ["node", c]
            elif c.endswith(".sh"):
                return ["bash", c]
    return None

def test_adversarial_corpus():
    executable = get_executable()
    assert executable is not None, "Could not find filter_payload script (.py, .js, or .sh) in /home/user/"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))

    assert len(clean_files) > 0, f"No clean JSON files found in {clean_dir}"
    assert len(evil_files) > 0, f"No evil JSON files found in {evil_dir}"

    clean_failed = []
    for f in clean_files:
        res = subprocess.run(executable + [f], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(f))

    evil_bypassed = []
    for f in evil_files:
        res = subprocess.run(executable + [f], capture_output=True)
        if res.returncode == 0:
            evil_bypassed.append(os.path.basename(f))

    error_messages = []
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean rejected: {', '.join(clean_failed)}")
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    assert not error_messages, " | ".join(error_messages)