# test_final_state.py

import os
import subprocess
import numpy as np
import pytest

def compute_target_load():
    """
    Re-computes the target average load directly from the video file
    using the exact ffmpeg pipeline described in the task.
    """
    video_path = "/app/server_load.mp4"
    if not os.path.exists(video_path):
        return 62.35  # Fallback target if video is missing

    cmd = [
        "ffmpeg", "-i", video_path, 
        "-f", "image2pipe", 
        "-pix_fmt", "gray", 
        "-vcodec", "rawvideo", "-"
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    total_sum = 0
    frame_count = 0
    frame_size = 640 * 480

    while True:
        raw = proc.stdout.read(frame_size)
        if not raw or len(raw) < frame_size:
            break
        frame = np.frombuffer(raw, dtype=np.uint8).reshape((480, 640))
        # Center 100x100 region: x from 270 to 369, y from 190 to 289
        center = frame[190:290, 270:370]
        total_sum += np.sum(center)
        frame_count += 1

    proc.stdout.close()
    proc.wait()

    if frame_count == 0:
        return 0.0

    avg_intensity = total_sum / (frame_count * 100 * 100)
    return (avg_intensity / 255.0) * 100

def test_timezone_configuration():
    bashrc_path = "/home/user/.bashrc"
    assert os.path.exists(bashrc_path), f"File missing: {bashrc_path}"
    with open(bashrc_path, "r") as f:
        content = f.read()
    assert "TZ" in content and "Etc/UTC" in content, "TZ=Etc/UTC not configured properly in /home/user/.bashrc"

def test_average_load_metric():
    file_path = "/home/user/average_load.txt"
    assert os.path.exists(file_path), f"Output file missing: {file_path}"

    with open(file_path, "r") as f:
        try:
            val = float(f.read().strip())
        except ValueError:
            pytest.fail("Could not parse float from /home/user/average_load.txt")

    target = compute_target_load()
    tolerance = 0.5

    assert abs(val - target) <= tolerance, f"Computed load {val} is not within {tolerance} of the target {target:.2f}"

def test_scheduled_task_setup():
    script_path = "/home/user/monitor.sh"
    cron_path = "/home/user/monitor.cron"

    assert os.path.exists(script_path), f"Script missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

    assert os.path.exists(cron_path), f"Cron file missing: {cron_path}"
    with open(cron_path, "r") as f:
        cron_content = f.read()

    # Check for correct schedule: 2:30 AM every day
    assert "30 2 * * *" in cron_content, "Cron schedule is not set to 2:30 AM every day (expected '30 2 * * *')"
    assert "/home/user/monitor.sh" in cron_content, "Cron file does not execute /home/user/monitor.sh"