# test_final_state.py

import os
import re
import subprocess
import pytest

FILTER_BIN = "/home/user/qemu_net_filter"
LOG_FILE = "/home/user/filter.log"
LOGROTATE_CONF = "/home/user/logrotate.conf"
CLEAN_DIR = "/app/corpus/clean"
EVIL_DIR = "/app/corpus/evil"

def test_filter_executable_exists():
    assert os.path.exists(FILTER_BIN), f"Filter binary missing at {FILTER_BIN}"
    assert os.path.isfile(FILTER_BIN), f"{FILTER_BIN} is not a file"
    assert os.access(FILTER_BIN, os.X_OK), f"{FILTER_BIN} is not executable"

def test_filter_behavior_and_logging():
    # Ensure log file is empty or doesn't exist before we start to cleanly check new entries
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]

    clean_failures = []
    evil_failures = []

    for fpath in clean_files:
        res = subprocess.run([FILTER_BIN, fpath], capture_output=True)
        if res.returncode != 0:
            clean_failures.append(os.path.basename(fpath))

    for fpath in evil_files:
        res = subprocess.run([FILTER_BIN, fpath], capture_output=True)
        if res.returncode == 0:
            evil_failures.append(os.path.basename(fpath))

    errors = []
    if clean_failures:
        errors.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures[:5])}...")
    if evil_failures:
        errors.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failures[:5])}...")

    assert not errors, " | ".join(errors)

    # Validate log file
    assert os.path.exists(LOG_FILE), f"Log file {LOG_FILE} was not created"

    with open(LOG_FILE, "r") as f:
        log_lines = f.read().strip().split("\n")

    expected_logs_count = len(clean_files) + len(evil_files)
    assert len(log_lines) >= expected_logs_count, f"Expected at least {expected_logs_count} log lines, found {len(log_lines)}"

    log_pattern = re.compile(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] .* - (ACCEPTED|REJECTED)$")
    invalid_logs = [line for line in log_lines if not log_pattern.match(line)]

    assert not invalid_logs, f"Found {len(invalid_logs)} invalid log lines. Example: {invalid_logs[0]}"

def test_logrotate_config():
    assert os.path.exists(LOGROTATE_CONF), f"Logrotate config missing at {LOGROTATE_CONF}"

    # Check syntax
    res = subprocess.run(["logrotate", "-d", LOGROTATE_CONF], capture_output=True, text=True)
    assert res.returncode == 0, f"logrotate config syntax error: {res.stderr}"

    with open(LOGROTATE_CONF, "r") as f:
        content = f.read()

    # Check required directives (ignoring whitespace and comments)
    content_no_comments = re.sub(r"#.*", "", content)

    assert re.search(r"\bdaily\b", content_no_comments), "Logrotate config missing 'daily' directive"
    assert re.search(r"\brotate\s+5\b", content_no_comments), "Logrotate config missing 'rotate 5' directive"
    assert re.search(r"\bcompress\b", content_no_comments), "Logrotate config missing 'compress' directive"
    assert re.search(r"\bcreate\s+0?644\b", content_no_comments), "Logrotate config missing 'create 0644' directive"