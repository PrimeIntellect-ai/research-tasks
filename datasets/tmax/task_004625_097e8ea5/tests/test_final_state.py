# test_final_state.py

import os
import re
import glob
import subprocess
import concurrent.futures
import pytest

SCRIPT_PATH = "/home/user/sanitizer.py"
EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
AUDIT_LOG_PATH = "/home/user/audit.log"

def run_sanitizer(filepath):
    """Run the sanitizer script on a given file and return the exit code."""
    result = subprocess.run(
        ["python3", SCRIPT_PATH, filepath],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return filepath, result.returncode

def test_sanitizer_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Sanitizer script not found at {SCRIPT_PATH}"

def test_adversarial_corpus():
    assert os.path.isdir(EVIL_CORPUS_DIR), f"Evil corpus dir missing: {EVIL_CORPUS_DIR}"
    assert os.path.isdir(CLEAN_CORPUS_DIR), f"Clean corpus dir missing: {CLEAN_CORPUS_DIR}"

    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*"))
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*"))

    assert len(evil_files) > 0, "No files found in evil corpus."
    assert len(clean_files) > 0, "No files found in clean corpus."

    # Clear audit log before running to ensure clean state for our test
    if os.path.exists(AUDIT_LOG_PATH):
        os.remove(AUDIT_LOG_PATH)

    all_files = evil_files + clean_files

    # Run concurrently to test file locking
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_file = {executor.submit(run_sanitizer, f): f for f in all_files}
        for future in concurrent.futures.as_completed(future_to_file):
            filepath, returncode = future.result()
            results[filepath] = returncode

    # Check evil files
    evil_bypassed = [f for f in evil_files if results[f] != 1]

    # Check clean files
    clean_modified = [f for f in clean_files if results[f] != 0]

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {[os.path.basename(f) for f in evil_bypassed]}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {[os.path.basename(f) for f in clean_modified]}")

    assert not error_msgs, " | ".join(error_msgs)

    # Check audit log
    assert os.path.isfile(AUDIT_LOG_PATH), f"Audit log not created at {AUDIT_LOG_PATH}"

    with open(AUDIT_LOG_PATH, "r") as f:
        log_lines = f.read().splitlines()

    assert len(log_lines) == len(all_files), f"Expected {len(all_files)} lines in audit log, found {len(log_lines)}."

    # Regex to match audit log format: [<ISO8601_TIMESTAMP>] <filepath> <REJECTED|CLEAN>
    # Note: ISO8601 can vary, but typically YYYY-MM-DDTHH:MM:SS.mmmmmm
    log_regex = re.compile(r"^\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?\] /app/corpus/(evil|clean)/[^ ]+ (REJECTED|CLEAN)$")

    invalid_lines = [line for line in log_lines if not log_regex.match(line)]
    assert not invalid_lines, f"Found {len(invalid_lines)} invalid or corrupted lines in audit log, indicating possible file locking failure. First invalid line: {invalid_lines[0] if invalid_lines else ''}"