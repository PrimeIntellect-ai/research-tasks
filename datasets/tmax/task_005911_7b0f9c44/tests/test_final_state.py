# test_final_state.py

import os
import tarfile
import filecmp

def test_curated_art_001():
    incoming_path = "/home/user/incoming/art_001.tar.gz"
    curated_path = "/home/user/curated/art_001.tar.gz"

    assert os.path.isfile(curated_path), f"Expected file {curated_path} was not found."
    assert filecmp.cmp(incoming_path, curated_path, shallow=False), f"File {curated_path} does not match the original {incoming_path}."

def test_curated_art_002_logs():
    curated_path = "/home/user/curated/art_002_logs.tar.bz2"
    assert os.path.isfile(curated_path), f"Expected file {curated_path} was not found."

    try:
        with tarfile.open(curated_path, "r:bz2") as tar:
            member = tar.getmember("logs/info.log")
            f = tar.extractfile(member)
            content = f.read().decode("utf-8").strip()
            assert "Log data for art_002" in content, f"Incorrect content in logs/info.log for art_002: {content}"
    except Exception as e:
        assert False, f"Failed to read {curated_path} as a valid bzip2 tarball: {e}"

def test_curated_art_004_logs():
    curated_path = "/home/user/curated/art_004_logs.tar.bz2"
    assert os.path.isfile(curated_path), f"Expected file {curated_path} was not found."

    try:
        with tarfile.open(curated_path, "r:bz2") as tar:
            member = tar.getmember("logs/info.log")
            f = tar.extractfile(member)
            content = f.read().decode("utf-8").strip()
            assert "Log data for art_004" in content, f"Incorrect content in logs/info.log for art_004: {content}"
    except Exception as e:
        assert False, f"Failed to read {curated_path} as a valid bzip2 tarball: {e}"

def test_curated_no_art_003():
    curated_dir = "/home/user/curated"
    for filename in os.listdir(curated_dir):
        assert "art_003" not in filename, f"Artifact art_003 should have been dropped, but found: {filename}"

def test_curation_log():
    log_path = "/home/user/curation.log"
    assert os.path.isfile(log_path), f"Log file {log_path} was not found."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = {
        "[keep] Processed art_001.tar.gz",
        "[extract_logs] Processed art_002.tar.gz",
        "[extract_logs] Processed art_004.tar.gz"
    }

    actual_lines = set(lines)

    missing = expected_lines - actual_lines
    extra = actual_lines - expected_lines

    assert not missing, f"Log file is missing expected entries: {missing}"
    assert not extra, f"Log file contains unexpected entries: {extra}"

def test_no_temp_files():
    curated_dir = "/home/user/curated"
    for filename in os.listdir(curated_dir):
        assert not filename.endswith(".tmp"), f"Found a temporary file {filename} in {curated_dir}. Atomic writes should rename these."