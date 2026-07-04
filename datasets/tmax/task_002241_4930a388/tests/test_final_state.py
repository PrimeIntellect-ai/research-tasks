# test_final_state.py
import os
import subprocess
import pytest

def test_project_summary_log():
    log_path = "/home/user/project_summary.log"
    assert os.path.isfile(log_path), f"Missing {log_path}"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, f"Expected at least 2 lines in {log_path}, found {len(lines)}"

    # Part 1: Video Metadata Recovery
    assert lines[0] == "42", f"Expected first line of {log_path} to be '42', got '{lines[0]}'"

    # Part 3: Final Output
    assert lines[1] == "/home/user/sanitizer", f"Expected second line of {log_path} to be '/home/user/sanitizer', got '{lines[1]}'"

def test_sanitizer_executable_exists():
    executable_path = "/home/user/sanitizer"
    assert os.path.isfile(executable_path), f"Missing executable: {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable"

def test_sanitizer_adversarial_corpus():
    executable_path = "/home/user/sanitizer"
    clean_dir = "/app/corpora/clean/"
    evil_dir = "/app/corpora/evil/"

    assert os.path.isdir(clean_dir), f"Missing clean corpus directory: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Missing evil corpus directory: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    modified_clean = []
    bypassed_evil = []

    for cf in clean_files:
        result = subprocess.run([executable_path, cf], capture_output=True)
        if result.returncode != 0:
            modified_clean.append(os.path.basename(cf))

    for ef in evil_files:
        result = subprocess.run([executable_path, ef], capture_output=True)
        if result.returncode != 1:
            bypassed_evil.append(os.path.basename(ef))

    errors = []
    if modified_clean:
        errors.append(f"{len(modified_clean)} of {len(clean_files)} clean modified (rejected): {', '.join(modified_clean)}")
    if bypassed_evil:
        errors.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed (accepted): {', '.join(bypassed_evil)}")

    assert not errors, "\n".join(errors)