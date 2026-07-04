# test_final_state.py

import os
import time
import fcntl

def test_doc_daemon_exists():
    assert os.path.exists("/home/user/doc_daemon.go"), "The file /home/user/doc_daemon.go does not exist."

def test_test_doc_processed():
    processed_path = "/home/user/processed_docs/test_doc.md"
    assert os.path.exists(processed_path), f"The processed file {processed_path} does not exist. Did the daemon process the initial test file?"

    with open(processed_path, "r") as f:
        content = f.read()

    expected_content = (
        "# Welcome to Acme Corp\n"
        "This document is CONFIDENTIAL - DO NOT DISTRIBUTE.\n"
        "Please keep it safe.\n\n"
        "---\n"
        "Processed by DocWatchdog"
    )

    assert content.strip() == expected_content.strip(), f"The content of {processed_path} does not match the expected output."

def test_daemon_live_processing_with_lock():
    raw_path = "/home/user/raw_docs/eval_doc.md"
    processed_path = "/home/user/processed_docs/eval_doc.md"

    # Ensure processed file doesn't exist yet
    if os.path.exists(processed_path):
        os.remove(processed_path)

    # Write to raw_docs while holding a lock
    with open(raw_path, "w") as f:
        # Acquire exclusive lock
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)

        f.write("{{COMPANY_NAME}} Annual Report\nStatus: {{STATUS}}\n")
        f.flush()

        # Hold the lock for 2 seconds to test daemon's wait capability
        time.sleep(2)

        # Release lock
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    # Wait for the daemon to process the file
    time.sleep(2)

    assert os.path.exists(processed_path), "The daemon failed to process a newly created file (eval_doc.md) after it was unlocked."

    with open(processed_path, "r") as f:
        content = f.read()

    expected_content = (
        "Acme Corp Annual Report\n"
        "Status: CONFIDENTIAL - DO NOT DISTRIBUTE\n\n"
        "---\n"
        "Processed by DocWatchdog"
    )

    assert content.strip() == expected_content.strip(), "The content of the dynamically processed eval_doc.md does not match the expected output."