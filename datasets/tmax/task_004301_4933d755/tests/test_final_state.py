# test_final_state.py

import os
import subprocess
import pytest

EVIL_CORPUS_DIR = "/home/user/tests/evil_corpus/"
CLEAN_CORPUS_DIR = "/home/user/tests/clean_corpus/"
BINARY_PATH = "/home/user/app/filter_paths"

def run_filter_paths(filepath):
    try:
        result = subprocess.run(
            [BINARY_PATH, filepath],
            capture_output=True,
            text=True,
            timeout=2
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"ERROR: {e}"

def test_binary_exists():
    assert os.path.isfile(BINARY_PATH), f"Compiled binary missing at {BINARY_PATH}. Did you run gcc?"
    assert os.access(BINARY_PATH, os.X_OK), f"Binary at {BINARY_PATH} is not executable."

def test_adversarial_corpus():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Missing evil corpus dir: {EVIL_CORPUS_DIR}"
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Missing clean corpus dir: {CLEAN_CORPUS_DIR}"

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]

    assert len(evil_files) > 0, "No files found in evil corpus."
    assert len(clean_files) > 0, "No files found in clean corpus."

    bypassed_evil = []
    modified_clean = []

    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        output = run_filter_paths(filepath)
        if output != "MALICIOUS":
            bypassed_evil.append((filename, output))

    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        output = run_filter_paths(filepath)
        if output != "SAFE":
            modified_clean.append((filename, output))

    error_messages = []
    if bypassed_evil:
        files_list = ", ".join([f"{f} (got {out})" for f, out in bypassed_evil[:5]])
        error_messages.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {files_list}")

    if modified_clean:
        files_list = ", ".join([f"{f} (got {out})" for f, out in modified_clean[:5]])
        error_messages.append(f"{len(modified_clean)} of {len(clean_files)} clean modified (rejected): {files_list}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))

def test_watcher_process_restarted():
    pid_file = "/home/user/app/watcher.pid"
    assert os.path.isfile(pid_file), "watcher.pid is missing."
    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"Invalid PID in watcher.pid: {pid_str}"
    pid = int(pid_str)

    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Watcher process with PID {pid} is not running. Did you restart the watcher.sh script?")