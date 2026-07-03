# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/sanitizer.py"

def test_sanitizer_exists():
    assert os.path.exists(SCRIPT_PATH), f"Sanitizer script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"Path {SCRIPT_PATH} is not a file"

def run_sanitizer(input_content):
    return subprocess.run(
        ["python3", SCRIPT_PATH],
        input=input_content,
        text=True,
        capture_output=True
    )

def test_clean_corpus():
    clean_dirs = ["/home/user/corpus/clean", "/app/test_corpus/clean"]
    failed_files = []
    total_files = 0

    for clean_dir in clean_dirs:
        if not os.path.exists(clean_dir):
            continue
        for filename in os.listdir(clean_dir):
            if not filename.endswith(".sql"):
                continue
            filepath = os.path.join(clean_dir, filename)
            total_files += 1
            with open(filepath, "r") as f:
                content = f.read()

            result = run_sanitizer(content)

            if result.returncode != 0 or result.stdout.strip() != content.strip():
                failed_files.append(filepath)

    assert total_files > 0, "No clean corpus files found to test."
    if failed_files:
        pytest.fail(f"{len(failed_files)} of {total_files} clean files modified or rejected. Offending files: {', '.join(os.path.basename(f) for f in failed_files)}")

def test_evil_corpus():
    evil_dirs = ["/home/user/corpus/evil", "/app/test_corpus/evil"]
    failed_files = []
    total_files = 0

    for evil_dir in evil_dirs:
        if not os.path.exists(evil_dir):
            continue
        for filename in os.listdir(evil_dir):
            if not filename.endswith(".sql"):
                continue
            filepath = os.path.join(evil_dir, filename)
            total_files += 1
            with open(filepath, "r") as f:
                content = f.read()

            result = run_sanitizer(content)

            if result.returncode != 1 or result.stdout.strip() != "REJECTED":
                failed_files.append(filepath)

    assert total_files > 0, "No evil corpus files found to test."
    if failed_files:
        pytest.fail(f"{len(failed_files)} of {total_files} evil files bypassed. Offending files: {', '.join(os.path.basename(f) for f in failed_files)}")