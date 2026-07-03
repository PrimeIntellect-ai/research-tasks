# test_final_state.py

import os
import subprocess
import pytest
import shutil

PAYLOAD_PATH = "/home/user/payload.archive"
SOURCE_DIR = "/home/user/source_data"
LAYOUT_CONF = "/home/user/layout.conf"
EXTRACT_DIR = "/home/user/extracted"
ARCHIVER_PATH = "/app/archiver"

def test_payload_exists_and_size():
    assert os.path.exists(PAYLOAD_PATH), f"Payload archive not found at {PAYLOAD_PATH}"
    size = os.path.getsize(PAYLOAD_PATH)
    assert size <= 25000, f"Payload archive too large: {size} bytes (must be <= 25000 bytes)"

def test_extraction_and_contents():
    assert os.path.exists(PAYLOAD_PATH), f"Payload archive not found at {PAYLOAD_PATH}"

    # Clean up and recreate extraction directory
    if os.path.exists(EXTRACT_DIR):
        shutil.rmtree(EXTRACT_DIR)
    os.makedirs(EXTRACT_DIR)

    # Run the legacy extraction tool
    result = subprocess.run(
        [ARCHIVER_PATH, "extract", PAYLOAD_PATH, EXTRACT_DIR],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Archiver failed with return code {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"

    # Verify contents against layout.conf
    assert os.path.exists(LAYOUT_CONF), f"Missing layout configuration: {LAYOUT_CONF}"

    with open(LAYOUT_CONF, 'r') as f:
        lines = f.read().splitlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if '=' not in line:
            continue

        dest_rel, src_name = line.split('=', 1)

        # Calculate absolute destination path (resolving ../ traversals)
        dest_abs = os.path.normpath(os.path.join(EXTRACT_DIR, dest_rel))
        src_abs = os.path.join(SOURCE_DIR, src_name)

        assert os.path.exists(dest_abs), f"Missing extracted file: {dest_abs} (derived from {dest_rel})"

        # Compare file contents to ensure correct extraction and deduplication
        with open(src_abs, 'rb') as f_src, open(dest_abs, 'rb') as f_dest:
            src_data = f_src.read()
            dest_data = f_dest.read()
            assert src_data == dest_data, f"Content mismatch for {dest_abs}. Expected contents of {src_abs}."