# test_final_state.py

import os
import glob
import subprocess
import pytest

SCRIPT_PATH = "/home/user/auditor.py"
LOG_PATH = "/home/user/audit_trail.log"
CLEAN_DIR = "/app/corpora/clean/"
EVIL_DIR = "/app/corpora/evil/"

def run_auditor(target_dir):
    if os.path.exists(LOG_PATH):
        os.remove(LOG_PATH)

    result = subprocess.run(
        ["python3", SCRIPT_PATH, target_dir],
        capture_output=True,
        text=True
    )
    return result

def parse_audit_log():
    if not os.path.exists(LOG_PATH):
        return {}

    results = {}
    with open(LOG_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(" ", 1)
            if len(parts) == 2:
                status, filepath = parts
                results[filepath] = status
    return results

def test_auditor_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Auditor script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"

def test_clean_corpus_accepted():
    clean_files = glob.glob(os.path.join(CLEAN_DIR, "*.json"))
    assert len(clean_files) > 0, "No clean corpus files found to test."

    run_auditor(CLEAN_DIR)

    assert os.path.exists(LOG_PATH), f"Audit log not created at {LOG_PATH} after processing clean corpus."

    log_results = parse_audit_log()

    rejected_clean = []
    missing_clean = []

    for cf in clean_files:
        if cf not in log_results:
            missing_clean.append(cf)
        elif log_results[cf] != "[ACCEPT]":
            rejected_clean.append(cf)

    error_msgs = []
    if missing_clean:
        error_msgs.append(f"{len(missing_clean)} clean files were not logged. Examples: {missing_clean[:3]}")
    if rejected_clean:
        error_msgs.append(f"{len(rejected_clean)} of {len(clean_files)} clean files were incorrectly REJECTED. Examples: {rejected_clean[:3]}")

    assert not error_msgs, " | ".join(error_msgs)

def test_evil_corpus_rejected():
    evil_files = glob.glob(os.path.join(EVIL_DIR, "*.json"))
    assert len(evil_files) > 0, "No evil corpus files found to test."

    run_auditor(EVIL_DIR)

    assert os.path.exists(LOG_PATH), f"Audit log not created at {LOG_PATH} after processing evil corpus."

    log_results = parse_audit_log()

    accepted_evil = []
    missing_evil = []

    for ef in evil_files:
        if ef not in log_results:
            missing_evil.append(ef)
        elif log_results[ef] != "[REJECT]":
            accepted_evil.append(ef)

    error_msgs = []
    if missing_evil:
        error_msgs.append(f"{len(missing_evil)} evil files were not logged. Examples: {missing_evil[:3]}")
    if accepted_evil:
        error_msgs.append(f"{len(accepted_evil)} of {len(evil_files)} evil files bypassed the filter and were ACCEPTED. Examples: {accepted_evil[:3]}")

    assert not error_msgs, " | ".join(error_msgs)