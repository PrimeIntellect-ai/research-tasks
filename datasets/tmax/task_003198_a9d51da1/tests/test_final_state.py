# test_final_state.py

import os
import subprocess
import glob
import pytest

def get_expected_redaction(input_str):
    """
    Derives the expected redacted string based on the rules discovered during reverse engineering.
    """
    tokens = input_str.split(' ')
    out = []
    skip_next = False

    for t in tokens:
        if skip_next:
            out.append("[REDACTED]")
            skip_next = False
            continue

        if t in ['--db-pass', '-K']:
            out.append(t)
            skip_next = True
        elif t.startswith('--auth-token='):
            out.append('--auth-token=[REDACTED]')
        else:
            out.append(t)

    if skip_next:
        out.append("[REDACTED]")

    return ' '.join(out)

def test_redactor_exists_and_executable():
    """Verify the student compiled the redactor to the correct path and it is executable."""
    redactor_path = "/home/user/redactor"
    assert os.path.exists(redactor_path), f"Redactor binary not found at {redactor_path}"
    assert os.path.isfile(redactor_path), f"Expected a file at {redactor_path}, but found something else."
    assert os.access(redactor_path, os.X_OK), f"Redactor binary at {redactor_path} is not executable."

def test_corpus_extracted():
    """Verify the student successfully extracted the corpus."""
    clean_dir = "/home/user/corpus/clean"
    evil_dir = "/home/user/corpus/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus directory not found at {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory not found at {evil_dir}"

    clean_files = glob.glob(os.path.join(clean_dir, "*"))
    evil_files = glob.glob(os.path.join(evil_dir, "*"))

    assert len(clean_files) > 0, "No files found in clean corpus directory. Extraction may have failed."
    assert len(evil_files) > 0, "No files found in evil corpus directory. Extraction may have failed."

def test_clean_corpus_preserved():
    """Verify that the redactor leaves clean corpus files completely unchanged."""
    redactor_path = "/home/user/redactor"
    clean_files = glob.glob("/home/user/corpus/clean/*")

    # Skip test if corpus isn't extracted properly (handled by previous test)
    if not clean_files:
        pytest.skip("Clean corpus files not found.")

    failed_files = []
    for filepath in clean_files:
        with open(filepath, 'r') as f:
            original_content = f.read()

        proc = subprocess.run([redactor_path], input=original_content, text=True, capture_output=True)

        if proc.returncode != 0 or proc.stdout != original_content:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified: {', '.join(failed_files)}")

def test_evil_corpus_redacted():
    """Verify that the redactor correctly identifies and redacts sensitive values in the evil corpus."""
    redactor_path = "/home/user/redactor"
    evil_files = glob.glob("/home/user/corpus/evil/*")

    if not evil_files:
        pytest.skip("Evil corpus files not found.")

    failed_files = []
    for filepath in evil_files:
        with open(filepath, 'r') as f:
            original_content = f.read()

        expected_content = get_expected_redaction(original_content)

        proc = subprocess.run([redactor_path], input=original_content, text=True, capture_output=True)

        if proc.returncode != 0 or proc.stdout != expected_content:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed: {', '.join(failed_files)}")