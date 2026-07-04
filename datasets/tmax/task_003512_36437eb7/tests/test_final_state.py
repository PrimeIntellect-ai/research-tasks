# test_final_state.py

import os
import subprocess
import filecmp
import shutil
import pytest

def test_final_state():
    archive_path = "/home/user/surveillance.dedup"
    raw_frames_dir = "/home/user/raw_frames"
    unpack_dir = "/home/user/unpacked_frames"
    archiver_bin = "/home/user/archiver"

    assert os.path.exists(archive_path), f"Archive file not found at {archive_path}."
    assert os.path.exists(archiver_bin), f"Archiver binary not found at {archiver_bin}."
    assert os.path.exists(raw_frames_dir), f"Raw frames directory not found at {raw_frames_dir}."

    # 1. Check Verify command
    verify_proc = subprocess.run([archiver_bin, "verify", archive_path], capture_output=True)
    assert verify_proc.returncode == 0, f"Archiver verify command failed with exit code {verify_proc.returncode}. stderr: {verify_proc.stderr.decode('utf-8', errors='ignore')}"

    # 2. Unpack
    if os.path.exists(unpack_dir):
        shutil.rmtree(unpack_dir)
    os.makedirs(unpack_dir, exist_ok=True)

    unpack_proc = subprocess.run([archiver_bin, "unpack", archive_path, unpack_dir], capture_output=True)
    assert unpack_proc.returncode == 0, f"Archiver unpack command failed with exit code {unpack_proc.returncode}. stderr: {unpack_proc.stderr.decode('utf-8', errors='ignore')}"

    # 3. Verify exact extraction matches
    raw_files = sorted(os.listdir(raw_frames_dir))
    unpacked_files = sorted(os.listdir(unpack_dir))

    assert raw_files, "No raw frames found in raw_frames directory."

    # Check naming convention
    for f in raw_files:
        assert f.startswith("cam_A_frame_") and f.endswith(".png"), f"File {f} does not match the required naming pattern 'cam_A_frame_<N>.png'."

    assert raw_files == unpacked_files, "Unpacked filenames do not match raw frames."

    total_raw_size = 0
    for f in raw_files:
        raw_path = os.path.join(raw_frames_dir, f)
        unp_path = os.path.join(unpack_dir, f)
        assert filecmp.cmp(raw_path, unp_path, shallow=False), f"File content mismatch for {f}"
        total_raw_size += os.path.getsize(raw_path)

    # 4. Compute metric
    assert total_raw_size > 0, "Total size of raw frames is 0."
    archive_size = os.path.getsize(archive_path)
    compression_ratio = archive_size / total_raw_size

    assert compression_ratio < 0.25, f"Compression ratio {compression_ratio:.4f} is not strictly less than 0.25."