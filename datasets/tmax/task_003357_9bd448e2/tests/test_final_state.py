# test_final_state.py

import os
import glob
import subprocess
import pytest

def find_cli():
    """Find the scanner-cli binary, preferring debug but falling back to release."""
    debug_path = "/home/user/scanner/target/debug/scanner-cli"
    release_path = "/home/user/scanner/target/release/scanner-cli"
    if os.path.isfile(debug_path):
        return debug_path
    if os.path.isfile(release_path):
        return release_path
    return None

def test_adversarial_corpus():
    """
    Test the scanner-cli against the adversarial corpus.
    Evil files must be rejected (print 'EVIL').
    Clean files must be accepted (print 'SAFE').
    """
    cli_path = find_cli()
    assert cli_path is not None, "scanner-cli binary not found in /home/user/scanner/target/debug/ or release/"

    evil_dir = "/app/corpus/evil"
    clean_dir = "/app/corpus/clean"

    evil_files = glob.glob(os.path.join(evil_dir, "*.pld"))
    clean_files = glob.glob(os.path.join(clean_dir, "*.pld"))

    assert len(evil_files) > 0, "No evil corpus files found."
    assert len(clean_files) > 0, "No clean corpus files found."

    evil_bypassed = []
    clean_modified = []

    server_addr = "http://127.0.0.1:50051"

    # Test evil corpus
    for f in evil_files:
        try:
            result = subprocess.run(
                [cli_path, server_addr, f],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = result.stdout.strip()
            if output != "EVIL":
                evil_bypassed.append(f"{os.path.basename(f)} (got {output!r})")
        except Exception as e:
            evil_bypassed.append(f"{os.path.basename(f)} (error: {e})")

    # Test clean corpus
    for f in clean_files:
        try:
            result = subprocess.run(
                [cli_path, server_addr, f],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = result.stdout.strip()
            if output != "SAFE":
                clean_modified.append(f"{os.path.basename(f)} (got {output!r})")
        except Exception as e:
            clean_modified.append(f"{os.path.basename(f)} (error: {e})")

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")

    assert not errors, " | ".join(errors)