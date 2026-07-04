# test_final_state.py

import os
import subprocess
import pytest

def test_transcript():
    transcript_path = "/home/user/transcript.txt"
    assert os.path.exists(transcript_path), f"Missing required file: {transcript_path}"

    with open(transcript_path, "r") as f:
        content = f.read().strip().lower()

    # Remove punctuation just in case the student left some
    import string
    content = content.translate(str.maketrans('', '', string.punctuation))

    assert "the system is compromised" in content, f"Transcript does not contain the expected text. Found: {content}"

def test_sanitizer_executable():
    executable_path = "/home/user/wav_sanitizer"
    assert os.path.exists(executable_path), f"Missing executable: {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File is not executable: {executable_path}"

def test_sanitizer_clean_corpus():
    executable_path = "/home/user/wav_sanitizer"
    clean_dir = "/app/corpus/clean/"

    assert os.path.exists(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(clean_files) > 0, "No files found in clean corpus."

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run([executable_path, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files were incorrectly rejected (exit code != 0): {', '.join(failed_files)}")

def test_sanitizer_evil_corpus():
    executable_path = "/home/user/wav_sanitizer"
    evil_dir = "/app/corpus/evil/"

    assert os.path.exists(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(evil_files) > 0, "No files found in evil corpus."

    bypassed_files = []
    for filepath in evil_files:
        result = subprocess.run([executable_path, filepath], capture_output=True)
        if result.returncode != 1:
            bypassed_files.append(os.path.basename(filepath))

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed the sanitizer (exit code != 1): {', '.join(bypassed_files)}")