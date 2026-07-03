# test_final_state.py

import os
import re
import stat
import time
import shutil
import resource
import subprocess
import pytest

def test_scripts_exist_and_executable():
    scripts = [
        "/home/user/video_toolkit/build.sh",
        "/home/user/pipeline.sh",
        "/home/user/prop_test.sh"
    ]
    for script in scripts:
        assert os.path.isfile(script), f"Script {script} does not exist."
        st = os.stat(script)
        assert bool(st.st_mode & stat.S_IXUSR), f"Script {script} is not executable."

def test_prop_test_report():
    report_path = "/home/user/test_report.txt"

    # If the report doesn't exist, try running the prop_test.sh script
    if not os.path.exists(report_path):
        subprocess.run(["/home/user/prop_test.sh"], check=True, cwd="/home/user")

    assert os.path.isfile(report_path), f"Report file {report_path} was not created."

    with open(report_path, "r") as f:
        content = f.read().strip()

    match = re.search(r"Success:\s*(\d+),\s*Segfaults:\s*(\d+)", content)
    assert match is not None, f"Report content '{content}' does not match expected format 'Success: X, Segfaults: Y'."

    successes = int(match.group(1))
    segfaults = int(match.group(2))
    total = successes + segfaults
    assert total == 100, f"Expected 100 total tests, but got {total} (Success: {successes}, Segfaults: {segfaults})."

def test_pipeline_execution_and_metrics():
    pipeline_script = "/home/user/pipeline.sh"
    video_path = "/app/traffic.mp4"
    frames_dir = "/home/user/frames"
    log_path = "/home/user/processing.log"

    # Clean up previous runs if any
    if os.path.exists(frames_dir):
        shutil.rmtree(frames_dir)
    if os.path.exists(log_path):
        os.remove(log_path)

    os.makedirs(frames_dir, exist_ok=True)

    # Measure resource usage and time
    ru_before = resource.getrusage(resource.RUSAGE_CHILDREN)
    t0 = time.time()

    result = subprocess.run([pipeline_script, video_path], capture_output=True, text=True)

    t1 = time.time()
    ru_after = resource.getrusage(resource.RUSAGE_CHILDREN)

    assert result.returncode == 0, f"Pipeline script failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

    # Calculate metrics
    wall_clock_time = t1 - t0
    cpu_time_user = ru_after.ru_utime - ru_before.ru_utime
    cpu_time_sys = ru_after.ru_stime - ru_before.ru_stime
    total_cpu_time = cpu_time_user + cpu_time_sys

    # Assert CPU time metric (<= 1.0s)
    assert total_cpu_time <= 1.0, f"Total CPU time {total_cpu_time:.3f}s exceeded threshold of 1.0s. The optimized library may not be linked correctly."

    # Assert rate limiting (50 frames at 5 FPS should take ~10 seconds)
    assert wall_clock_time >= 9.0, f"Wall-clock time {wall_clock_time:.3f}s is too fast. Rate limiting to 5 FPS was likely not implemented correctly."

    # Verify outputs
    assert os.path.isfile(log_path), f"Log file {log_path} was not created."
    with open(log_path, "r") as f:
        lines = [line for line in f.read().splitlines() if line.strip()]

    assert len(lines) == 50, f"Expected 50 lines in {log_path}, got {len(lines)}."

    frames_created = [f for f in os.listdir(frames_dir) if f.endswith(".jpg")]
    assert len(frames_created) == 50, f"Expected 50 frames created in {frames_dir}, got {len(frames_created)}."