# test_final_state.py

import os
import subprocess
import pytest

def test_libwalrec_builds_successfully():
    """Verify that the vendored package builds successfully after fixing the Makefile."""
    build_dir = "/app/libwalrec"

    # Run make clean to ensure a fresh build
    subprocess.run(["make", "clean"], cwd=build_dir, capture_output=True)

    # Run make
    result = subprocess.run(["make"], cwd=build_dir, capture_output=True, text=True)

    assert result.returncode == 0, f"make failed in {build_dir}. Output: {result.stderr}"

    # Check if libwalrec.a was created
    archive_path = os.path.join(build_dir, "libwalrec.a")
    assert os.path.isfile(archive_path), f"Expected build artifact {archive_path} was not created."

def test_wal_sanitizer_adversarial_corpus():
    """Verify that the wal_sanitizer correctly rejects evil files and accepts clean files."""
    sanitizer_bin = "/home/user/wal_sanitizer"

    assert os.path.isfile(sanitizer_bin), f"Sanitizer binary not found at {sanitizer_bin}"
    assert os.access(sanitizer_bin, os.X_OK), f"Sanitizer at {sanitizer_bin} is not executable."

    evil_dir = "/app/corpora/evil"
    clean_dir = "/app/corpora/clean"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    assert len(evil_files) > 0, "No files found in evil corpus."
    assert len(clean_files) > 0, "No files found in clean corpus."

    bypassed_evil = []
    for filepath in evil_files:
        result = subprocess.run([sanitizer_bin, filepath], capture_output=True)
        if result.returncode != 1:
            bypassed_evil.append(os.path.basename(filepath))

    modified_clean = []
    for filepath in clean_files:
        result = subprocess.run([sanitizer_bin, filepath], capture_output=True)
        if result.returncode != 0:
            modified_clean.append(os.path.basename(filepath))

    error_msgs = []
    if bypassed_evil:
        error_msgs.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        error_msgs.append(f"{len(modified_clean)} of {len(clean_files)} clean modified: {', '.join(modified_clean)}")

    assert not error_msgs, " | ".join(error_msgs)