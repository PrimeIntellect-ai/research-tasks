# test_final_state.py

import os
import subprocess
import tempfile
import pytest

BINARY_PATH = "/home/user/safe_archiver/target/release/safe_archiver"
CLEAN_CORPUS_DIR = "/home/user/corpus/clean"
EVIL_CORPUS_DIR = "/home/user/corpus/evil"
LEGACY_UNPACKER = "/app/legacy_unpacker"

def test_binary_exists():
    assert os.path.isfile(BINARY_PATH), f"Compiled binary not found at {BINARY_PATH}"
    assert os.access(BINARY_PATH, os.X_OK), f"Binary at {BINARY_PATH} is not executable"

def test_clean_corpus():
    if not os.path.isdir(CLEAN_CORPUS_DIR):
        pytest.skip("Clean corpus directory not found")

    clean_dirs = [os.path.join(CLEAN_CORPUS_DIR, d) for d in os.listdir(CLEAN_CORPUS_DIR) if os.path.isdir(os.path.join(CLEAN_CORPUS_DIR, d))]

    failed_clean = []

    for cdir in clean_dirs:
        with tempfile.TemporaryDirectory() as tmpdir:
            archive_path = os.path.join(tmpdir, "archive.bkp")
            result = subprocess.run([BINARY_PATH, cdir, archive_path], capture_output=True, text=True)

            if result.returncode != 0:
                failed_clean.append(os.path.basename(cdir))
                continue

            # verify archive with legacy unpacker
            unpack_dir = os.path.join(tmpdir, "unpacked")
            os.makedirs(unpack_dir)
            unpack_res = subprocess.run([LEGACY_UNPACKER, archive_path, unpack_dir], capture_output=True)
            if unpack_res.returncode != 0:
                failed_clean.append(f"{os.path.basename(cdir)} (invalid archive format)")

    assert not failed_clean, f"{len(failed_clean)} of {len(clean_dirs)} clean directories failed or produced invalid archives: {', '.join(failed_clean)}"

def test_evil_corpus():
    if not os.path.isdir(EVIL_CORPUS_DIR):
        pytest.skip("Evil corpus directory not found")

    evil_dirs = [os.path.join(EVIL_CORPUS_DIR, d) for d in os.listdir(EVIL_CORPUS_DIR) if os.path.isdir(os.path.join(EVIL_CORPUS_DIR, d))]

    bypassed_evil = []

    for edir in evil_dirs:
        with tempfile.TemporaryDirectory() as tmpdir:
            archive_path = os.path.join(tmpdir, "archive.bkp")
            result = subprocess.run([BINARY_PATH, edir, archive_path], capture_output=True, text=True)

            if result.returncode == 0:
                bypassed_evil.append(os.path.basename(edir))

    assert not bypassed_evil, f"{len(bypassed_evil)} of {len(evil_dirs)} evil directories bypassed the check: {', '.join(bypassed_evil)}"