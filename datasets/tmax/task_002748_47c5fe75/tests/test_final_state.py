# test_final_state.py

import os
import shutil
import subprocess
import pytest
import re

def test_adversarial_corpus():
    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"
    test_input = "/app/corpora/test_input"
    test_output = "/home/user/test_output"

    # Ensure directories exist
    os.makedirs(test_input, exist_ok=True)
    os.makedirs(test_output, exist_ok=True)

    # Clear test_input and test_output if they already have files
    for d in [test_input, test_output]:
        for f in os.listdir(d):
            os.remove(os.path.join(d, f))

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.json')]
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.json')]

    # Copy corpus to test_input
    for f in clean_files:
        shutil.copy(os.path.join(clean_dir, f), os.path.join(test_input, f))
    for f in evil_files:
        shutil.copy(os.path.join(evil_dir, f), os.path.join(test_input, f))

    # Run the agent's tool
    assert os.path.isdir("/home/user/log_filter"), "Agent's log_filter directory does not exist."
    result = subprocess.run(
        ["cargo", "run", "--release", "--", test_input, test_output],
        cwd="/home/user/log_filter",
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Agent's tool failed to run. Stderr: {result.stderr}\nStdout: {result.stdout}"

    output_files = set(os.listdir(test_output))

    clean_bypassed = []
    for f in clean_files:
        if f not in output_files:
            clean_bypassed.append(f)
        else:
            with open(os.path.join(clean_dir, f), 'r') as orig, open(os.path.join(test_output, f), 'r') as out:
                if orig.read().strip() != out.read().strip():
                    clean_bypassed.append(f + " (modified)")

    evil_bypassed = []
    for f in evil_files:
        if f in output_files:
            evil_bypassed.append(f)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_bypassed:
        errors.append(f"{len(clean_bypassed)} of {len(clean_files)} clean modified or missing: {', '.join(clean_bypassed)}")

    assert not errors, " | ".join(errors)

def test_video_report():
    report_path = "/home/user/report.md"
    assert os.path.exists(report_path), f"Report file not found at {report_path}."

    with open(report_path, 'r') as f:
        content = f.read()

    assert "Traffic Analysis Report" in content, "Missing report title 'Traffic Analysis Report'."
    assert re.search(r"Processed \d+ frames", content, re.IGNORECASE), "Missing processed frames count (e.g., 'Processed 15 frames')."
    assert re.search(r"Window 0-4s: \d+ bytes", content, re.IGNORECASE), "Missing 'Window 0-4s: [Sum] bytes' in report."
    assert re.search(r"Window 5-9s: \d+ bytes", content, re.IGNORECASE), "Missing 'Window 5-9s: [Sum] bytes' in report."