# test_final_state.py

import os
import subprocess
import pytest

def test_phase1_error_frame():
    """Verify that the correct error frame was identified and written to the file."""
    error_frame_path = "/home/user/error_frame.txt"
    assert os.path.isfile(error_frame_path), f"File missing: {error_frame_path}"

    with open(error_frame_path, "r") as f:
        content = f.read().strip()

    assert content in ["14", "15"], f"Expected frame 14 or 15 in {error_frame_path}, but got: '{content}'"

def test_phase2_go_race():
    """Verify that the Go dispatcher passes data race checks."""
    dispatcher_dir = "/home/user/dispatcher"
    assert os.path.isdir(dispatcher_dir), f"Directory missing: {dispatcher_dir}"

    result = subprocess.run(
        ["go", "test", "-race"],
        cwd=dispatcher_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Go test failed or race condition detected:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_phase3_manifest_validator():
    """Verify that the Rust manifest validator correctly accepts clean files and rejects evil files."""
    binary_path = "/home/user/manifest_validator/target/release/manifest_validator"
    assert os.path.isfile(binary_path), f"Rust binary missing at {binary_path}. Did you compile with --release?"
    assert os.access(binary_path, os.X_OK), f"Rust binary is not executable at {binary_path}"

    evil_corpus = "/app/corpora/evil"
    clean_corpus = "/app/corpora/clean"

    evil_files = [os.path.join(evil_corpus, f) for f in os.listdir(evil_corpus) if os.path.isfile(os.path.join(evil_corpus, f))]
    clean_files = [os.path.join(clean_corpus, f) for f in os.listdir(clean_corpus) if os.path.isfile(os.path.join(clean_corpus, f))]

    assert len(evil_files) > 0, "No files found in evil corpus."
    assert len(clean_files) > 0, "No files found in clean corpus."

    bypassed_evil = []
    for f in evil_files:
        res = subprocess.run([binary_path, f], capture_output=True)
        if res.returncode == 0:
            bypassed_evil.append(os.path.basename(f))

    rejected_clean = []
    for f in clean_files:
        res = subprocess.run([binary_path, f], capture_output=True)
        if res.returncode != 0:
            rejected_clean.append(os.path.basename(f))

    errors = []
    if bypassed_evil:
        errors.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if rejected_clean:
        errors.append(f"{len(rejected_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(rejected_clean)}")

    assert not errors, "Manifest validator failed:\n" + "\n".join(errors)