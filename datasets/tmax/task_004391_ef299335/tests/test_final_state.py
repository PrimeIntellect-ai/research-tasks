# test_final_state.py

import os
import subprocess
import tarfile
import tempfile
import pytest

EXECUTABLE = "/home/user/dataset_filter"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"

def parse_config(filepath):
    config = {}
    with open(filepath, "r") as f:
        for line in f:
            if ": " in line:
                key, val = line.strip().split(": ", 1)
                config[key] = val
    return config

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE), f"Executable not found at {EXECUTABLE}"
    assert os.access(EXECUTABLE, os.X_OK), f"File at {EXECUTABLE} is not executable"

def test_evil_corpus_rejected():
    if not os.path.isfile(EXECUTABLE):
        pytest.fail("Executable not found")

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    bypassed = []

    for evil_file in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, evil_file)
        result = subprocess.run([EXECUTABLE, filepath], capture_output=True)
        if result.returncode != 1:
            bypassed.append(evil_file)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed)}")

def test_clean_corpus_accepted():
    if not os.path.isfile(EXECUTABLE):
        pytest.fail("Executable not found")

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    failed = []

    # Run in a temporary directory to not pollute the current working directory
    with tempfile.TemporaryDirectory() as tmpdir:
        for clean_file in clean_files:
            filepath = os.path.join(CLEAN_CORPUS_DIR, clean_file)
            config = parse_config(filepath)

            result = subprocess.run([EXECUTABLE, filepath], cwd=tmpdir, capture_output=True)
            if result.returncode != 0:
                failed.append(f"{clean_file} (exit code {result.returncode})")
                continue

            output_archive = config.get("output_archive")
            if not output_archive:
                failed.append(f"{clean_file} (no output_archive in config)")
                continue

            archive_path = os.path.join(tmpdir, output_archive)
            if not os.path.isfile(archive_path):
                failed.append(f"{clean_file} (archive {output_archive} not created)")
                continue

            try:
                start_frame = int(config["start_frame"])
                end_frame = int(config["end_frame"])
                expected_count = end_frame - start_frame

                with tarfile.open(archive_path, "r") as tar:
                    members = tar.getmembers()
                    if len(members) != expected_count:
                        failed.append(f"{clean_file} (expected {expected_count} frames, got {len(members)})")
            except Exception as e:
                failed.append(f"{clean_file} (error verifying archive: {e})")

    if failed:
        pytest.fail(f"{len(failed)} of {len(clean_files)} clean modified/failed: {', '.join(failed)}")