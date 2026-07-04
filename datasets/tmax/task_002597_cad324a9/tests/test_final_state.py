# test_final_state.py

import os
import json
import hashlib
import subprocess
import pytest
import numpy as np

VIDEO_PATH = "/app/experiment_record.mp4"
ARCHIVE_PATH = "/home/user/dataset.archive"
MANIFEST_PATH = "/home/user/manifest.json"

def get_raw_frames():
    """Extract 50 frames (5 seconds at 10 fps) as raw grayscale bytes."""
    cmd = [
        "ffmpeg", "-y", "-i", VIDEO_PATH,
        "-t", "5", "-r", "10",
        "-pix_fmt", "gray", "-f", "image2pipe",
        "-vcodec", "rawvideo", "-"
    ]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {stderr.decode('utf-8')}")

    return stdout

def test_archive_and_manifest():
    assert os.path.exists(ARCHIVE_PATH), f"Archive file missing: {ARCHIVE_PATH}"
    assert os.path.exists(MANIFEST_PATH), f"Manifest file missing: {MANIFEST_PATH}"

    with open(MANIFEST_PATH, "r") as f:
        manifest = json.load(f)

    assert len(manifest) == 5, "Manifest should contain exactly 5 chunks"

    raw_bytes = get_raw_frames()

    # We don't know the exact resolution, but we know there are 50 frames total.
    # So each frame is len(raw_bytes) // 50 bytes.
    total_size = len(raw_bytes)
    assert total_size > 0, "Failed to extract raw frames"

    chunk_size = total_size // 5

    for i in range(5):
        chunk_key = str(i)
        assert chunk_key in manifest, f"Chunk {i} missing from manifest"

        expected_chunk_bytes = raw_bytes[i * chunk_size : (i + 1) * chunk_size]
        expected_hash = hashlib.sha256(expected_chunk_bytes).hexdigest()

        assert manifest[chunk_key]["checksum"] == expected_hash, f"Checksum mismatch for chunk {i}"
        assert "offset" in manifest[chunk_key], f"Offset missing for chunk {i}"
        assert "size" in manifest[chunk_key], f"Size missing for chunk {i}"

    archive_size = os.path.getsize(ARCHIVE_PATH)
    max_allowed_size = total_size * 0.65

    assert archive_size <= max_allowed_size, f"Archive size {archive_size} exceeds allowed limit {max_allowed_size}"