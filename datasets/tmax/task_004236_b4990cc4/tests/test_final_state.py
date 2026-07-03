# test_final_state.py

import os
import glob
import subprocess
import time
import tarfile
import tempfile
import hashlib
import pytest

WAL_CHECK_BIN = "/home/user/wal_check/target/release/wal_check"

def test_wal_check_corpus():
    assert os.path.isfile(WAL_CHECK_BIN), f"Executable not found at {WAL_CHECK_BIN}"
    assert os.access(WAL_CHECK_BIN, os.X_OK), f"File at {WAL_CHECK_BIN} is not executable"

    clean_dir = "/opt/corpus/clean"
    evil_dir = "/opt/corpus/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failures = []
    for cf in clean_files:
        result = subprocess.run([WAL_CHECK_BIN, cf], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(cf))

    evil_failures = []
    for ef in evil_files:
        result = subprocess.run([WAL_CHECK_BIN, ef], capture_output=True)
        if result.returncode == 0:
            evil_failures.append(os.path.basename(ef))

    error_msg = []
    if evil_failures:
        error_msg.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_msg.append(f"{len(clean_failures)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failures)}")

    assert not error_msg, " ; ".join(error_msg)


def test_pipeline_end_to_end():
    # Clean up processed dir before starting
    processed_dir = "/home/user/run/spool/processed"
    os.makedirs(processed_dir, exist_ok=True)
    for f in glob.glob(os.path.join(processed_dir, "*.tar.gz")):
        os.remove(f)

    # Start services
    producer = subprocess.Popen(["python3", "/home/user/services/producer.py"])
    archiver = subprocess.Popen(["bash", "/home/user/services/archiver.sh"])

    try:
        time.sleep(12)
    finally:
        producer.terminate()
        archiver.terminate()
        producer.wait()
        archiver.wait()

    archives = glob.glob(os.path.join(processed_dir, "*.tar.gz"))
    assert archives, "No archives were produced in /home/user/run/spool/processed/"

    latest_archive = max(archives, key=os.path.getmtime)

    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(latest_archive, "r:gz") as tar:
            tar.extractall(path=tmpdir)

        extracted_files = os.listdir(tmpdir)

        assert "manifest.sha256" in extracted_files, "manifest.sha256 is missing from the archive root"

        wal_files = [f for f in extracted_files if f.endswith(".wal")]
        assert len(wal_files) > 0, "No .wal files found in the archive"

        # Verify manifest
        manifest_path = os.path.join(tmpdir, "manifest.sha256")
        with open(manifest_path, "r") as f:
            manifest_lines = f.read().strip().splitlines()

        manifest_dict = {}
        for line in manifest_lines:
            parts = line.split()
            if len(parts) >= 2:
                manifest_dict[os.path.basename(parts[1])] = parts[0]

        for wal_file in wal_files:
            wal_path = os.path.join(tmpdir, wal_file)

            # Checksum verification
            with open(wal_path, "rb") as f:
                content_bytes = f.read()
            actual_sha256 = hashlib.sha256(content_bytes).hexdigest()
            assert wal_file in manifest_dict, f"{wal_file} not found in manifest.sha256"
            assert manifest_dict[wal_file] == actual_sha256, f"Checksum mismatch for {wal_file}"

            # Content verification
            content_str = content_bytes.decode("utf-8", errors="ignore")
            lines = content_str.splitlines()

            assert lines, f"{wal_file} is empty"
            assert lines[0] == "WAL_START", f"{wal_file} missing WAL_START at the beginning"
            assert lines[-1] == "WAL_END", f"{wal_file} missing WAL_END at the end"

            assert "../" not in content_str, f"{wal_file} contains path traversal attempt '../'"
            assert "EXEC=" not in content_str, f"{wal_file} contains malicious execution attempt 'EXEC='"