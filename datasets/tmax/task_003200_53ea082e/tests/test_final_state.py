# test_final_state.py

import os
import re
import subprocess
import glob
import pytest

def test_transcript_content():
    """Verify the audio transcription is reasonably accurate."""
    transcript_path = "/home/user/transcript.txt"
    assert os.path.isfile(transcript_path), f"Transcript file missing at {transcript_path}"

    with open(transcript_path, "r", encoding="utf-8") as f:
        content = f.read().strip().lower()

    expected_words = [
        "warning", "backup", "rotation", "system", "vulnerable", 
        "path", "traversal", "attacks", "check", "symlink", "targets", "immediately"
    ]

    # Remove punctuation from content for easier matching
    clean_content = re.sub(r'[^\w\s]', '', content)

    matched_words = sum(1 for word in expected_words if word in clean_content)
    # Allow for minor transcription errors (e.g. 10 out of 12 words)
    assert matched_words >= len(expected_words) - 2, \
        f"Transcript does not sufficiently match the expected audio content. Found: '{content}'"

def test_tar_sanitizer_evil_corpus():
    """Verify the Go sanitizer correctly rejects all evil tar files."""
    go_script = "/home/user/tar_sanitizer.go"
    assert os.path.isfile(go_script), f"Go script missing at {go_script}"

    evil_dir = "/app/corpora/evil"
    evil_files = glob.glob(os.path.join(evil_dir, "*.tar"))
    assert evil_files, f"No tar files found in {evil_dir}"

    bypassed = []

    for tar_file in evil_files:
        result = subprocess.run(
            ["go", "run", go_script, tar_file],
            capture_output=True,
            text=True
        )
        stdout = result.stdout.strip()

        if result.returncode != 1 or stdout != "REJECT":
            bypassed.append((os.path.basename(tar_file), result.returncode, stdout))

    if bypassed:
        details = ", ".join([f"{f} (code: {c}, out: '{o}')" for f, c, o in bypassed])
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: {details}")

def test_tar_sanitizer_clean_corpus():
    """Verify the Go sanitizer correctly accepts all clean tar files."""
    go_script = "/home/user/tar_sanitizer.go"
    assert os.path.isfile(go_script), f"Go script missing at {go_script}"

    clean_dir = "/app/corpora/clean"
    clean_files = glob.glob(os.path.join(clean_dir, "*.tar"))
    assert clean_files, f"No tar files found in {clean_dir}"

    rejected = []

    for tar_file in clean_files:
        result = subprocess.run(
            ["go", "run", go_script, tar_file],
            capture_output=True,
            text=True
        )
        stdout = result.stdout.strip()

        if result.returncode != 0 or stdout != "ACCEPT":
            rejected.append((os.path.basename(tar_file), result.returncode, stdout))

    if rejected:
        details = ", ".join([f"{f} (code: {c}, out: '{o}')" for f, c, o in rejected])
        pytest.fail(f"{len(rejected)} of {len(clean_files)} clean modified/rejected: {details}")