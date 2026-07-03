# test_final_state.py

import os
import glob
import re
import subprocess
import tempfile

def test_video_frames():
    video_path = "/app/project_demo.mp4"
    frames_dir = "/home/user/frames"

    assert os.path.isfile(video_path), f"Video file missing at {video_path}"
    assert os.path.isdir(frames_dir), f"Frames directory missing at {frames_dir}"

    # Get video duration
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_path],
        capture_output=True, text=True
    )
    assert result.returncode == 0, "Failed to get video duration with ffprobe"

    try:
        duration = float(result.stdout.strip())
    except ValueError:
        pytest.fail(f"Could not parse duration from ffprobe output: {result.stdout}")

    duration_int = int(duration)

    frames = sorted(glob.glob(os.path.join(frames_dir, "frame_*.jpg")))
    assert len(frames) > 0, "No frames found in /home/user/frames/"

    # Allow a small margin of error for frame extraction depending on exact video length and ffmpeg rounding
    assert abs(len(frames) - duration_int) <= 2, f"Expected around {duration_int} frames based on video length, got {len(frames)}"

    for i, frame_path in enumerate(frames, start=1):
        basename = os.path.basename(frame_path)
        assert re.match(r"^frame_\d{4}\.jpg$", basename), f"Frame name {basename} does not match expected format"
        expected_name = f"frame_{i:04d}.jpg"
        assert basename == expected_name, f"Frames not sequentially named correctly: expected {expected_name}, got {basename}"

def test_safe_tar_evil_corpus():
    binary = "/home/user/safe_tar/target/release/safe_tar"
    assert os.path.isfile(binary), f"Compiled binary missing at {binary}"
    assert os.access(binary, os.X_OK), f"Binary at {binary} is not executable"

    evil_dir = "/app/corpus/evil"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing at {evil_dir}"

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.tar')]
    assert len(evil_files) > 0, "No evil tar files found to test against"

    failed = []
    for f in evil_files:
        tar_path = os.path.join(evil_dir, f)
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run([binary, tar_path, tmpdir], capture_output=True, text=True)
            stdout = result.stdout.strip()

            if result.returncode != 1 or stdout != "REJECT":
                failed.append(f"{f} (exit code {result.returncode}, stdout: {stdout})")
            elif os.listdir(tmpdir):
                failed.append(f"{f} (output directory not empty after rejection)")

    assert not failed, f"{len(failed)} of {len(evil_files)} evil bypassed: {', '.join(failed)}"

def test_safe_tar_clean_corpus():
    binary = "/home/user/safe_tar/target/release/safe_tar"
    assert os.path.isfile(binary), f"Compiled binary missing at {binary}"

    clean_dir = "/app/corpus/clean"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing at {clean_dir}"

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.tar')]
    assert len(clean_files) > 0, "No clean tar files found to test against"

    failed = []
    for f in clean_files:
        tar_path = os.path.join(clean_dir, f)
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run([binary, tar_path, tmpdir], capture_output=True, text=True)
            stdout = result.stdout.strip()

            if result.returncode != 0 or stdout != "ACCEPT":
                failed.append(f"{f} (exit code {result.returncode}, stdout: {stdout})")
            elif not os.listdir(tmpdir):
                failed.append(f"{f} (output directory empty after acceptance)")

    assert not failed, f"{len(failed)} of {len(clean_files)} clean modified/rejected: {', '.join(failed)}"