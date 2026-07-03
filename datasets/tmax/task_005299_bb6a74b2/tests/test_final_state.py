# test_final_state.py

import os
import subprocess
import glob

def test_sanitizer_exists():
    assert os.path.exists("/home/user/sanitizer.py"), "Sanitizer script missing at /home/user/sanitizer.py"

def test_evil_corpus():
    evil_files = glob.glob("/opt/evaluation/evil/*.jsonl")
    assert evil_files, "No evil corpus files found in /opt/evaluation/evil/"

    bypassed = []

    for fpath in evil_files:
        result = subprocess.run(
            ["python3", "/home/user/sanitizer.py", fpath],
            capture_output=True,
            text=True
        )

        output = result.stdout.strip()
        if output:
            # If anything is printed, it means some evil lines bypassed the filter
            bypassed.append(os.path.basename(fpath))

    assert not bypassed, f"{len(bypassed)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(bypassed)}"

def test_clean_corpus():
    clean_files = glob.glob("/opt/evaluation/clean/*.jsonl")
    assert clean_files, "No clean corpus files found in /opt/evaluation/clean/"

    modified = []

    for fpath in clean_files:
        with open(fpath, "r", encoding="utf-8") as f:
            expected = f.read().strip()

        result = subprocess.run(
            ["python3", "/home/user/sanitizer.py", fpath],
            capture_output=True,
            text=True
        )

        output = result.stdout.strip()
        if output != expected:
            # If the output doesn't match exactly, the clean logs were modified or dropped
            modified.append(os.path.basename(fpath))

    assert not modified, f"{len(modified)} of {len(clean_files)} clean modified. Offending files: {', '.join(modified)}"