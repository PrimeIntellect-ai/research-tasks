# test_final_state.py

import os
import subprocess
import socket
import re
import pytest

def test_patch_sanitizer_adversarial_corpus():
    """
    Test the patch sanitizer against the evil and clean corpora.
    Pass requires rejecting all evil patches (exit code 1) and accepting all clean patches (exit code 0).
    """
    sanitizer_path = '/home/user/patch_sanitizer.py'
    assert os.path.isfile(sanitizer_path), f"Sanitizer script missing at {sanitizer_path}"

    clean_corpus_path = '/app/corpora/clean_patches/'
    evil_corpus_path = '/app/corpora/evil_patches/'

    assert os.path.isdir(clean_corpus_path), f"Clean corpus missing at {clean_corpus_path}"
    assert os.path.isdir(evil_corpus_path), f"Evil corpus missing at {evil_corpus_path}"

    clean_files = [os.path.join(clean_corpus_path, f) for f in os.listdir(clean_corpus_path) if os.path.isfile(os.path.join(clean_corpus_path, f))]
    evil_files = [os.path.join(evil_corpus_path, f) for f in os.listdir(evil_corpus_path) if os.path.isfile(os.path.join(evil_corpus_path, f))]

    assert len(clean_files) > 0, "No files found in clean corpus."
    assert len(evil_files) > 0, "No files found in evil corpus."

    clean_failed = []
    for f in clean_files:
        result = subprocess.run(['python3', sanitizer_path, f], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(f))

    evil_failed = []
    for f in evil_files:
        result = subprocess.run(['python3', sanitizer_path, f], capture_output=True)
        if result.returncode != 1:
            evil_failed.append(os.path.basename(f))

    errors = []
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified: {', '.join(clean_failed)}")

    assert not errors, " | ".join(errors)

def test_websocket_server_running():
    """
    Test that the server is listening on 127.0.0.1:8765.
    """
    port = 8765
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)
    try:
        result = s.connect_ex(('127.0.0.1', port))
        assert result == 0, f"Could not connect to WebSocket server on port {port}. Is the server running?"
    finally:
        s.close()

def test_memory_report():
    """
    Test that the memory report exists and the peak memory is strictly less than 50 MB.
    """
    report_path = '/home/user/memory_report.log'
    assert os.path.isfile(report_path), f"Memory report missing at {report_path}"

    with open(report_path, 'r') as f:
        content = f.read().strip()

    # Match format: Peak Memory: <X> MB
    match = re.search(r'Peak Memory:\s*([0-9]*\.?[0-9]+)\s*MB', content, re.IGNORECASE)
    assert match is not None, f"Could not parse Peak Memory from {report_path}. File content: '{content}'"

    peak_memory = float(match.group(1))
    assert peak_memory < 50.0, f"Peak memory {peak_memory} MB is not strictly less than the 50.0 MB limit."