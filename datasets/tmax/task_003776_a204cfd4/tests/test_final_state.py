# test_final_state.py

import os
import subprocess
import re
from pathlib import Path

def test_alert_filter_exists_and_executable():
    filter_path = Path("/home/user/alert_filter")
    assert filter_path.exists(), f"Expected compiled binary {filter_path} does not exist."
    assert filter_path.is_file(), f"Expected {filter_path} to be a file."
    assert os.access(filter_path, os.X_OK), f"Expected {filter_path} to be executable."

def test_alert_filter_corpus():
    clean_dir = Path("/app/corpus/clean")
    evil_dir = Path("/app/corpus/evil")
    filter_bin = "/home/user/alert_filter"

    clean_fails = []
    clean_total = 0
    if clean_dir.exists():
        for file_path in clean_dir.iterdir():
            if file_path.is_file():
                clean_total += 1
                with open(file_path, "r") as f:
                    content = f.read()
                proc = subprocess.run([filter_bin], input=content, text=True, capture_output=True)
                if proc.stdout != content:
                    clean_fails.append(file_path.name)

    evil_fails = []
    evil_total = 0
    if evil_dir.exists():
        for file_path in evil_dir.iterdir():
            if file_path.is_file():
                evil_total += 1
                with open(file_path, "r") as f:
                    content = f.read()
                proc = subprocess.run([filter_bin], input=content, text=True, capture_output=True)
                if proc.stdout != "":
                    evil_fails.append(file_path.name)

    error_messages = []
    if clean_fails:
        error_messages.append(f"{len(clean_fails)} of {clean_total} clean modified/rejected. Offending: {', '.join(clean_fails)}")
    if evil_fails:
        error_messages.append(f"{len(evil_fails)} of {evil_total} evil bypassed. Offending: {', '.join(evil_fails)}")

    assert not error_messages, "Corpus validation failed: " + "; ".join(error_messages)

def test_supervise_script_contents():
    script_path = Path("/home/user/supervise.sh")
    assert script_path.exists(), f"Expected script {script_path} does not exist."
    assert script_path.is_file(), f"Expected {script_path} to be a file."

    with open(script_path, "r") as f:
        content = f.read()

    # Check for directory creation
    assert "/app/run" in content, "Script does not appear to reference /app/run directory."

    # Check for symlink
    assert "ln -s" in content and "/app/run/upstream.sock" in content and "/home/user/active_socket" in content, \
        "Script does not contain the required symlink command for active_socket."

    # Check for SSH tunnel
    assert "ssh " in content and "-L" in content and "8080:localhost:80" in content, \
        "Script does not contain the required SSH tunnel command."

    # Check for infinite loop and daemon execution
    assert re.search(r"while\s+(true|:)", content) is not None, "Script does not contain an infinite while loop."
    assert "/app/upstream_daemon" in content, "Script does not invoke /app/upstream_daemon."