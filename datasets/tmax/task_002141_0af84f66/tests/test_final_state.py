# test_final_state.py

import os
import subprocess
import shutil
import glob
import tempfile
import pytest

def test_videdit_executable_exists():
    videdit_path = "/home/user/videdit/videdit"
    assert os.path.isfile(videdit_path), f"Executable not found at {videdit_path}"
    assert os.access(videdit_path, os.X_OK), f"File at {videdit_path} is not executable"

def test_libvalidator_exists():
    lib_path = "/home/user/videdit/libvalidator.so"
    assert os.path.isfile(lib_path), f"Shared library not found at {lib_path}"

def test_adversarial_corpus_check():
    videdit_path = "/home/user/videdit/videdit"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_patches = glob.glob(os.path.join(clean_dir, "*.patch"))
    evil_patches = glob.glob(os.path.join(evil_dir, "*.patch"))

    assert len(clean_patches) > 0, "No clean patches found to test against."
    assert len(evil_patches) > 0, "No evil patches found to test against."

    with tempfile.TemporaryDirectory() as temp_dir:
        for p in clean_patches + evil_patches:
            shutil.copy(p, temp_dir)

        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = "/home/user/videdit:" + env.get("LD_LIBRARY_PATH", "")

        result = subprocess.run(
            [videdit_path, "check", temp_dir],
            capture_output=True,
            text=True,
            env=env
        )

        output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]

        results_map = {}
        for line in output_lines:
            if ":" in line:
                fname, status = line.split(":", 1)
                results_map[fname.strip()] = status.strip()

        clean_modified = []
        for p in clean_patches:
            basename = os.path.basename(p)
            if results_map.get(basename) != "CLEAN":
                clean_modified.append(basename)

        evil_bypassed = []
        for p in evil_patches:
            basename = os.path.basename(p)
            if results_map.get(basename) != "EVIL":
                evil_bypassed.append(basename)

        error_msgs = []
        if evil_bypassed:
            error_msgs.append(f"{len(evil_bypassed)} of {len(evil_patches)} evil bypassed: {', '.join(evil_bypassed)}")
        if clean_modified:
            error_msgs.append(f"{len(clean_modified)} of {len(clean_patches)} clean modified (rejected): {', '.join(clean_modified)}")

        assert not error_msgs, " | ".join(error_msgs)

def test_thumbnail_extraction():
    videdit_path = "/home/user/videdit/videdit"
    video_path = "/app/video.mp4"

    with tempfile.TemporaryDirectory() as temp_dir:
        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = "/home/user/videdit:" + env.get("LD_LIBRARY_PATH", "")

        result = subprocess.run(
            [videdit_path, "thumb", video_path],
            cwd=temp_dir,
            capture_output=True,
            text=True,
            env=env
        )

        assert "Thumbnail extracted" in result.stdout, "Expected 'Thumbnail extracted' in stdout"

        thumb_path = os.path.join(temp_dir, "thumb.jpg")
        assert os.path.isfile(thumb_path), "thumb.jpg was not created in the working directory"

        # Basic check to ensure it's a JPEG
        with open(thumb_path, "rb") as f:
            header = f.read(2)
            assert header == b"\xff\xd8", "Extracted thumb.jpg is not a valid JPEG file"