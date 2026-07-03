# test_final_state.py

import os
import tarfile
import subprocess
import glob
import pytest

def test_frames_extracted():
    frames_dir = "/home/user/frames"
    assert os.path.isdir(frames_dir), f"Directory {frames_dir} is missing."

    frames = sorted(glob.glob(os.path.join(frames_dir, "frame_*.jpg")))
    assert len(frames) == 15, f"Expected exactly 15 frames, found {len(frames)}."

    for i, frame in enumerate(frames, start=1):
        expected_name = f"frame_{i:03d}.jpg"
        actual_name = os.path.basename(frame)
        assert actual_name == expected_name, f"Expected frame name {expected_name}, got {actual_name}."

def test_archive_created_correctly():
    archive_path = "/home/user/reference_frames.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} is missing."

    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            members = tar.getnames()
            assert len(members) == 15, f"Expected 15 files in archive, found {len(members)}."
            for i in range(1, 16):
                expected_name = f"frame_{i:03d}.jpg"
                assert expected_name in members, f"File {expected_name} is missing from the archive root."
    except tarfile.ReadError:
        pytest.fail(f"Archive {archive_path} is not a valid or readable tar.gz file.")

def test_verify_archive_script():
    script_path = "/home/user/verify_archive.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith(".tar.gz")] if os.path.isdir(clean_dir) else []
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith(".tar.gz")] if os.path.isdir(evil_dir) else []

    clean_bypassed = []
    evil_bypassed = []

    # Test clean corpus
    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        result = subprocess.run(["bash", script_path, filepath], capture_output=True, text=True)
        if result.returncode != 0 or result.stdout.strip() != "CLEAN":
            clean_bypassed.append(filename)

    # Test evil corpus
    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        result = subprocess.run(["bash", script_path, filepath], capture_output=True, text=True)
        if result.returncode != 1 or result.stdout.strip() != "EVIL":
            evil_bypassed.append(filename)

    # Also test the generated reference archive as clean
    reference_archive = "/home/user/reference_frames.tar.gz"
    if os.path.isfile(reference_archive):
        result = subprocess.run(["bash", script_path, reference_archive], capture_output=True, text=True)
        if result.returncode != 0 or result.stdout.strip() != "CLEAN":
            clean_bypassed.append("reference_frames.tar.gz")

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_bypassed:
        total_clean = len(clean_files) + (1 if os.path.isfile(reference_archive) else 0)
        error_messages.append(f"{len(clean_bypassed)} of {total_clean} clean modified/rejected: {', '.join(clean_bypassed)}")

    assert not error_messages, " | ".join(error_messages)