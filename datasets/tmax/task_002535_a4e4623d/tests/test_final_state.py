# test_final_state.py

import os
import re
import subprocess
import pytest

def test_compromised_port_identified():
    """Verify that the student correctly identified the compromised port."""
    port_file = "/home/user/compromised_port.txt"
    assert os.path.isfile(port_file), f"Expected file not found at {port_file}"

    with open(port_file, "r") as f:
        content = f.read().strip()

    assert content == "41337", f"Incorrect port number identified: {content}"

def test_sanitizer_script_exists():
    """Verify that the sanitizer script was created at the correct location."""
    script_path = "/home/user/sanitizer.py"
    assert os.path.isfile(script_path), f"Sanitizer script not found at {script_path}"

def test_sanitizer_evil_corpus():
    """Verify that the sanitizer correctly rejects all malicious files."""
    script_path = "/home/user/sanitizer.py"
    evil_dir = "/app/corpora/evil/"
    assert os.path.isdir(evil_dir), f"Evil corpus directory not found at {evil_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.txt')]
    assert len(evil_files) > 0, "No evil corpus files found to test."

    bypassed_files = []

    for evil_file in evil_files:
        result = subprocess.run(
            ["python3", script_path, "--input", evil_file],
            capture_output=True,
            text=True
        )
        if result.returncode != 1:
            bypassed_files.append(os.path.basename(evil_file))

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_files)}")

def test_sanitizer_clean_corpus():
    """Verify that the sanitizer correctly processes and redacts clean files."""
    script_path = "/home/user/sanitizer.py"
    clean_dir = "/app/corpora/clean/"
    assert os.path.isdir(clean_dir), f"Clean corpus directory not found at {clean_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.txt')]
    assert len(clean_files) > 0, "No clean corpus files found to test."

    modified_files = []
    ssn_regex = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')

    for clean_file in clean_files:
        with open(clean_file, "r") as f:
            original_content = f.read()

        expected_content = ssn_regex.sub("[REDACTED]", original_content)

        result = subprocess.run(
            ["python3", script_path, "--input", clean_file],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            modified_files.append(f"{os.path.basename(clean_file)} (exit code {result.returncode})")
            continue

        # Strip trailing newlines for comparison just in case the script adds a newline
        if result.stdout.rstrip('\r\n') != expected_content.rstrip('\r\n'):
            modified_files.append(f"{os.path.basename(clean_file)} (output mismatch)")

    if modified_files:
        pytest.fail(f"{len(modified_files)} of {len(clean_files)} clean modified or failed: {', '.join(modified_files)}")