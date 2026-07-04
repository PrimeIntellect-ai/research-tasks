# test_final_state.py

import os
import subprocess
import tarfile
import pytest

def test_video_chunking():
    archive_dir = "/home/user/archive"
    assert os.path.isdir(archive_dir), f"Archive directory missing: {archive_dir}"

    expected_chunks = ["chunk_0.tar.gz", "chunk_1.tar.gz", "chunk_2.tar.gz"]
    for chunk in expected_chunks:
        chunk_path = os.path.join(archive_dir, chunk)
        assert os.path.isfile(chunk_path), f"Expected chunk missing: {chunk_path}"

        try:
            with tarfile.open(chunk_path, "r:gz") as tar:
                members = [m for m in tar.getmembers() if m.isfile()]
                assert len(members) == 5, f"Expected exactly 5 files in {chunk}, found {len(members)}"
        except tarfile.TarError as e:
            pytest.fail(f"Failed to open tarball {chunk_path}: {e}")

def test_classifier_clean_corpus():
    script_path = "/home/user/classifier.sh"
    assert os.path.isfile(script_path), f"Classifier script missing: {script_path}"

    clean_dir = "/app/test_corpora/clean"
    assert os.path.isdir(clean_dir), f"Hidden clean corpus directory missing: {clean_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(clean_files) > 0, f"No files found in {clean_dir}"

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run(["bash", script_path, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(failed_files)}")

def test_classifier_evil_corpus():
    script_path = "/home/user/classifier.sh"
    assert os.path.isfile(script_path), f"Classifier script missing: {script_path}"

    evil_dir = "/app/test_corpora/evil"
    assert os.path.isdir(evil_dir), f"Hidden evil corpus directory missing: {evil_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(evil_files) > 0, f"No files found in {evil_dir}"

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run(["bash", script_path, filepath], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil bypassed/accepted. Offending files: {', '.join(failed_files)}")