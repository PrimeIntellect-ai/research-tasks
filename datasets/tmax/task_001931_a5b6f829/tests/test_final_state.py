# test_final_state.py

import os
import stat
import subprocess
import tempfile
import pytest

DETECTOR_PATH = "/home/user/detector"
ZIP_PATH = "/app/corpus.zip"
PASSWORD = "b1s3ct_s3cr3t!"

def test_detector_exists_and_executable():
    assert os.path.exists(DETECTOR_PATH), f"Detector binary not found at {DETECTOR_PATH}"
    assert os.path.isfile(DETECTOR_PATH), f"{DETECTOR_PATH} is not a file"
    st = os.stat(DETECTOR_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"{DETECTOR_PATH} is not executable"

def test_detector_against_corpus():
    if not os.path.exists(DETECTOR_PATH):
        pytest.fail("Detector binary is missing.")

    with tempfile.TemporaryDirectory() as tmpdir:
        # Extract the corpus to a temporary directory to ensure we have pristine files
        res = subprocess.run(
            ["unzip", "-P", PASSWORD, ZIP_PATH, "-d", tmpdir],
            capture_output=True,
            text=True
        )
        assert res.returncode == 0, f"Failed to unzip corpus for testing: {res.stderr}"

        # Adjust paths if the zip contained a top-level 'corpus' directory
        clean_dir = os.path.join(tmpdir, "clean")
        evil_dir = os.path.join(tmpdir, "evil")
        if not os.path.exists(clean_dir) and os.path.exists(os.path.join(tmpdir, "corpus", "clean")):
            clean_dir = os.path.join(tmpdir, "corpus", "clean")
            evil_dir = os.path.join(tmpdir, "corpus", "evil")

        assert os.path.exists(clean_dir), "Clean corpus directory not found in zip"
        assert os.path.exists(evil_dir), "Evil corpus directory not found in zip"

        clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
        evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

        assert len(clean_files) > 0, "No clean files found to test"
        assert len(evil_files) > 0, "No evil files found to test"

        clean_failed = []
        for cf in clean_files:
            res = subprocess.run([DETECTOR_PATH, cf], capture_output=True)
            if res.returncode != 0:
                clean_failed.append(os.path.basename(cf))

        evil_failed = []
        for ef in evil_files:
            res = subprocess.run([DETECTOR_PATH, ef], capture_output=True)
            if res.returncode == 0:
                evil_failed.append(os.path.basename(ef))

        errors = []
        if evil_failed:
            errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
        if clean_failed:
            errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failed)}")

        if errors:
            pytest.fail(" | ".join(errors))