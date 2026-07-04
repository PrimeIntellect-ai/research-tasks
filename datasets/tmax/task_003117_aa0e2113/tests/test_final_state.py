# test_final_state.py
import os
import subprocess
import pytest

def test_audit_filter_binary_exists():
    binary_path = "/home/user/audit_filter"
    source_path = "/home/user/audit_filter.c"
    assert os.path.isfile(source_path), f"Missing C source code at {source_path}"
    assert os.path.isfile(binary_path), f"Missing compiled binary at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary at {binary_path} is not executable"

def run_filter_on_corpus(binary_path, corpus_dir, expected_exit_code):
    if not os.path.isdir(corpus_dir):
        return # Skip if holdout doesn't exist in this environment

    files = [f for f in os.listdir(corpus_dir) if os.path.isfile(os.path.join(corpus_dir, f))]
    assert len(files) > 0, f"Corpus directory {corpus_dir} is empty"

    failed_files = []
    for f in files:
        file_path = os.path.join(corpus_dir, f)
        result = subprocess.run([binary_path, file_path], capture_output=True)
        if result.returncode != expected_exit_code:
            failed_files.append(f)

    return len(files), failed_files

def test_adversarial_corpus_clean():
    binary_path = "/home/user/audit_filter"
    clean_dirs = ["/app/corpus/clean", "/app/corpus/holdout_clean"]

    total_clean = 0
    all_failed = []

    for d in clean_dirs:
        if os.path.isdir(d):
            total, failed = run_filter_on_corpus(binary_path, d, 0)
            total_clean += total
            all_failed.extend([f"{d}/{f}" for f in failed])

    assert len(all_failed) == 0, f"{len(all_failed)} of {total_clean} clean modified/rejected. Offending files: {', '.join(all_failed[:10])}"

def test_adversarial_corpus_evil():
    binary_path = "/home/user/audit_filter"
    evil_dirs = ["/app/corpus/evil", "/app/corpus/holdout_evil"]

    total_evil = 0
    all_failed = []

    for d in evil_dirs:
        if os.path.isdir(d):
            total, failed = run_filter_on_corpus(binary_path, d, 1)
            total_evil += total
            all_failed.extend([f"{d}/{f}" for f in failed])

    assert len(all_failed) == 0, f"{len(all_failed)} of {total_evil} evil bypassed/accepted. Offending files: {', '.join(all_failed[:10])}"

def test_audit_trail_log():
    log_path = "/home/user/audit_trail.log"
    assert os.path.isfile(log_path), f"Missing audit log at {log_path}"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 100, f"Expected 100 entries in audit log, found {len(lines)}"

    clean_count = 0
    evil_count = 0

    for line in lines:
        if line.startswith("[CLEAN] /app/corpus/clean/"):
            clean_count += 1
        elif line.startswith("[EVIL] /app/corpus/evil/"):
            evil_count += 1
        else:
            pytest.fail(f"Invalid log entry format: {line}")

    assert clean_count == 50, f"Expected 50 [CLEAN] entries, found {clean_count}"
    assert evil_count == 50, f"Expected 50 [EVIL] entries, found {evil_count}"