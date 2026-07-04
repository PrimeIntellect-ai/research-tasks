# test_final_state.py

import os
import subprocess
import pytest

LOG_FILTER_SCRIPT = "/home/user/log_filter.sh"
LOGROTATE_CONF = "/home/user/logrotate.conf"
EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_CORPUS_DIR = "/app/corpus/clean"

def test_log_filter_script_exists_and_executable():
    assert os.path.isfile(LOG_FILTER_SCRIPT), f"Missing script: {LOG_FILTER_SCRIPT}"
    assert os.access(LOG_FILTER_SCRIPT, os.X_OK), f"Script is not executable: {LOG_FILTER_SCRIPT}"

def test_logrotate_conf():
    assert os.path.isfile(LOGROTATE_CONF), f"Missing logrotate config: {LOGROTATE_CONF}"

    with open(LOGROTATE_CONF, "r") as f:
        content = f.read()

    # Check for required directives
    assert "/home/user/logs/*.log" in content, "Missing target log files pattern in logrotate.conf"
    assert "daily" in content, "Missing 'daily' directive in logrotate.conf"
    assert "rotate 7" in content, "Missing 'rotate 7' directive in logrotate.conf"
    assert "compress" in content, "Missing 'compress' directive in logrotate.conf"
    assert "missingok" in content, "Missing 'missingok' directive in logrotate.conf"

def test_adversarial_corpus():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Missing evil corpus directory: {EVIL_CORPUS_DIR}"
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Missing clean corpus directory: {CLEAN_CORPUS_DIR}"

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus (expected exit code 1)
    for file_path in evil_files:
        result = subprocess.run(["bash", LOG_FILTER_SCRIPT, file_path], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(file_path))

    # Test clean corpus (expected exit code 0)
    for file_path in clean_files:
        result = subprocess.run(["bash", LOG_FILTER_SCRIPT, file_path], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(file_path))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")

    assert not error_messages, " | ".join(error_messages)