# test_final_state.py

import os
import subprocess
import tempfile
import glob
import shutil
import pytest

ORGANIZER_PATH = "/home/user/organizer"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"

def test_organizer_executable_exists():
    assert os.path.isfile(ORGANIZER_PATH), f"Executable not found at {ORGANIZER_PATH}"
    assert os.access(ORGANIZER_PATH, os.X_OK), f"File at {ORGANIZER_PATH} is not executable"

def test_adversarial_corpus():
    clean_archives = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.zres"))
    evil_archives = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.zres"))

    assert len(clean_archives) > 0, "No clean archives found to test."
    assert len(evil_archives) > 0, "No evil archives found to test."

    evil_bypassed = []
    clean_failed = []

    # Test Evil Corpus
    for archive in evil_archives:
        basename = os.path.basename(archive)
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [ORGANIZER_PATH, archive, tmpdir],
                capture_output=True,
                text=True
            )

            if result.returncode != 1 or "MALICIOUS ARCHIVE REJECTED" not in result.stdout:
                evil_bypassed.append(basename)

    # Test Clean Corpus
    for archive in clean_archives:
        basename = os.path.basename(archive)
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [ORGANIZER_PATH, archive, tmpdir],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                clean_failed.append(f"{basename} (exit code {result.returncode})")
                continue

            # Check that metadata.log was deleted
            if os.path.exists(os.path.join(tmpdir, "metadata.log")):
                clean_failed.append(f"{basename} (metadata.log not deleted)")
                continue

            # Check that files were actually extracted/renamed (directory not empty)
            extracted_files = os.listdir(tmpdir)
            if not extracted_files:
                clean_failed.append(f"{basename} (no files extracted)")

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_archives)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_archives)} clean modified/failed: {', '.join(clean_failed)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))

def test_library_patched():
    # Ensure the library source itself was patched to throw the exception
    zres_cpp_path = "/app/zres_lib-1.2.0/zres.cpp"
    assert os.path.isfile(zres_cpp_path), "zres.cpp is missing"

    with open(zres_cpp_path, "r") as f:
        content = f.read()

    assert "Path traversal detected" in content, "The library zres.cpp does not contain the required exception message 'Path traversal detected'."
    assert "throw" in content, "The library zres.cpp does not appear to throw an exception for path traversal."