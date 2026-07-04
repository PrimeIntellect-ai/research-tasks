# test_final_state.py

import os
import glob
import subprocess
import pytest

FILTER_SCRIPT = "/home/user/token_filter.py"
SANDBOX_SCRIPT = "/home/user/sandbox_test.sh"
CLEAN_DIR = "/app/corpora/clean"
EVIL_DIR = "/app/corpora/evil"

def test_sandbox_script_exists_and_valid():
    assert os.path.exists(SANDBOX_SCRIPT), f"Missing sandbox script at {SANDBOX_SCRIPT}"
    assert os.access(SANDBOX_SCRIPT, os.X_OK), f"Sandbox script {SANDBOX_SCRIPT} is not executable"

    with open(SANDBOX_SCRIPT, "r") as f:
        content = f.read()

    assert "bwrap" in content, "Sandbox script must use bwrap"
    assert "--unshare-all" in content, "Sandbox script must isolate network with --unshare-all"
    assert "--ro-bind" in content, "Sandbox script must mount directories read-only"

def test_token_filter_exists():
    assert os.path.exists(FILTER_SCRIPT), f"Missing token filter script at {FILTER_SCRIPT}"

def test_token_filter_correctness():
    clean_files = glob.glob(os.path.join(CLEAN_DIR, "*.txt"))
    evil_files = glob.glob(os.path.join(EVIL_DIR, "*.txt"))

    assert len(clean_files) > 0, "No clean files found"
    assert len(evil_files) > 0, "No evil files found"

    clean_bypassed = []
    evil_bypassed = []

    for fpath in clean_files:
        with open(fpath, "r") as f:
            token = f.read().strip()
        try:
            output = subprocess.check_output(
                ["python3", FILTER_SCRIPT, token], 
                text=True, 
                stderr=subprocess.STDOUT
            ).strip()
            if output != "CLEAN":
                clean_bypassed.append(os.path.basename(fpath))
        except subprocess.CalledProcessError:
            clean_bypassed.append(os.path.basename(fpath))

    for fpath in evil_files:
        with open(fpath, "r") as f:
            token = f.read().strip()
        try:
            output = subprocess.check_output(
                ["python3", FILTER_SCRIPT, token], 
                text=True, 
                stderr=subprocess.STDOUT
            ).strip()
            if output != "EVIL":
                evil_bypassed.append(os.path.basename(fpath))
        except subprocess.CalledProcessError:
            evil_bypassed.append(os.path.basename(fpath))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_bypassed:
        error_msgs.append(f"{len(clean_bypassed)} of {len(clean_files)} clean modified: {', '.join(clean_bypassed)}")

    assert not error_msgs, " | ".join(error_msgs)