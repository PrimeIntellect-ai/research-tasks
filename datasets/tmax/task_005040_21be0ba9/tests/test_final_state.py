# test_final_state.py

import os
import subprocess
import pytest

BINARY_PATH = "/home/user/path_filter"
SCRIPT_PATH = "/home/user/test_restores.sh"
CLEAN_DIR = "/app/hidden_tests/clean"
EVIL_DIR = "/app/hidden_tests/evil"

def run_filter(path_str):
    try:
        result = subprocess.run([BINARY_PATH, path_str], capture_output=True, text=True, timeout=2)
        return result.stdout.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "TIMEOUT", -1
    except Exception as e:
        return str(e), -1

def test_binary_exists_and_executable():
    assert os.path.isfile(BINARY_PATH), f"Compiled binary not found at {BINARY_PATH}"
    assert os.access(BINARY_PATH, os.X_OK), f"Binary at {BINARY_PATH} is not executable"

def test_clean_corpus():
    clean_failures = []
    total_clean = 0

    if os.path.isdir(CLEAN_DIR):
        for root, _, files in os.walk(CLEAN_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    for line in f:
                        line = line.strip('\n')
                        if not line:
                            continue
                        total_clean += 1
                        out, rc = run_filter(line)
                        if out != "ACCEPT" or rc != 0:
                            clean_failures.append(f"'{line}' (out: {out}, rc: {rc})")

    assert not clean_failures, f"{len(clean_failures)} of {total_clean} clean paths incorrectly rejected or failed: {clean_failures[:10]}"

def test_evil_corpus():
    evil_failures = []
    total_evil = 0

    if os.path.isdir(EVIL_DIR):
        for root, _, files in os.walk(EVIL_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    for line in f:
                        line = line.strip('\n')
                        if not line:
                            continue
                        total_evil += 1
                        out, rc = run_filter(line)
                        if out != "REJECT" or rc != 1:
                            evil_failures.append(f"'{line}' (out: {out}, rc: {rc})")

    assert not evil_failures, f"{len(evil_failures)} of {total_evil} evil paths incorrectly accepted or bypassed: {evil_failures[:10]}"

def test_automation_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Automation script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"