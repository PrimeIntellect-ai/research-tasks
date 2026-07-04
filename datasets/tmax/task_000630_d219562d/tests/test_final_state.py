# test_final_state.py
import os
import subprocess
import pytest

def test_reconstructed_timeline():
    timeline_path = "/home/user/reconstructed_timeline.log"
    assert os.path.isfile(timeline_path), f"File {timeline_path} is missing."

    expected_lines = []
    for svc in ['a', 'b', 'c']:
        log_file = f"/home/user/logs/service_{svc}.log"
        if os.path.isfile(log_file):
            with open(log_file, 'r') as f:
                for line in f:
                    if line.startswith("2023-10-01T00:00:"):
                        expected_lines.append(line.strip())

    expected_lines.sort()

    with open(timeline_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, "The reconstructed timeline does not match the expected chronologically sorted logs for the 00:00 minute."

def test_sanitizer_adversarial_corpus():
    sanitizer_bin = "/home/user/log_pipeline/build/sanitizer"
    assert os.path.isfile(sanitizer_bin), f"Sanitizer binary not found at {sanitizer_bin}"
    assert os.access(sanitizer_bin, os.X_OK), f"Sanitizer binary is not executable at {sanitizer_bin}"

    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    clean_failures = []
    evil_failures = []

    clean_count = 0
    if os.path.isdir(clean_dir):
        for fname in sorted(os.listdir(clean_dir)):
            clean_count += 1
            fpath = os.path.join(clean_dir, fname)
            with open(fpath, 'rb') as f:
                result = subprocess.run([sanitizer_bin], stdin=f, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if result.returncode != 0:
                    clean_failures.append(fname)

    evil_count = 0
    if os.path.isdir(evil_dir):
        for fname in sorted(os.listdir(evil_dir)):
            evil_count += 1
            fpath = os.path.join(evil_dir, fname)
            with open(fpath, 'rb') as f:
                result = subprocess.run([sanitizer_bin], stdin=f, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if result.returncode != 1:
                    evil_failures.append(fname)

    error_msg = []
    if clean_failures:
        error_msg.append(f"{len(clean_failures)} of {clean_count} clean modified/rejected: {', '.join(clean_failures)}")
    if evil_failures:
        error_msg.append(f"{len(evil_failures)} of {evil_count} evil bypassed/accepted: {', '.join(evil_failures)}")

    assert not error_msg, " | ".join(error_msg)