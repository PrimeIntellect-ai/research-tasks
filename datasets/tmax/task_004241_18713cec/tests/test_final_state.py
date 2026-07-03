# test_final_state.py

import os
import subprocess
import random
import pytest
import re

ORACLE_PATH = "/app/oracle_filter"
AGENT_PATH = "/home/user/anomaly_filter"
OUTPUT_FILE = "/home/user/brightness_anomalies.txt"
VIDEO_PATH = "/app/camera_feed.mp4"

def test_fuzz_equivalence():
    assert os.path.exists(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary not executable at {AGENT_PATH}"

    random.seed(42)
    for i in range(500):
        length = random.randint(1, 1000)
        nums = [random.uniform(0.0, 255.0) for _ in range(length)]
        input_data = "\n".join(f"{n:.6f}" for n in nums) + "\n"

        oracle_proc = subprocess.run([ORACLE_PATH], input=input_data, text=True, capture_output=True)
        agent_proc = subprocess.run([AGENT_PATH], input=input_data, text=True, capture_output=True)

        assert oracle_proc.returncode == 0, f"Oracle failed on fuzz iteration {i}"
        assert agent_proc.returncode == 0, f"Agent failed on fuzz iteration {i}"

        if oracle_proc.stdout != agent_proc.stdout:
            pytest.fail(f"Mismatch on fuzz iteration {i}.\nInput length: {length}\nOracle output start: {oracle_proc.stdout[:200]}\nAgent output start: {agent_proc.stdout[:200]}")

def test_brightness_anomalies_file():
    assert os.path.exists(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"

    # Extract brightness using ffmpeg signalstats
    cmd = ["ffmpeg", "-i", VIDEO_PATH, "-vf", "signalstats", "-f", "null", "-"]
    proc = subprocess.run(cmd, text=True, capture_output=True)

    # Parse YAVG from ffmpeg stderr
    yavgs = re.findall(r"YAVG=([0-9.]+)", proc.stderr)
    assert len(yavgs) > 0, "Failed to extract any YAVG values from the video using ffmpeg signalstats."

    input_data = "\n".join(yavgs) + "\n"

    oracle_proc = subprocess.run([ORACLE_PATH], input=input_data, text=True, capture_output=True)
    assert oracle_proc.returncode == 0, "Oracle failed to process the video brightness values."
    expected_output = oracle_proc.stdout

    with open(OUTPUT_FILE, "r") as f:
        actual_output = f.read()

    assert actual_output.strip() == expected_output.strip(), "The contents of brightness_anomalies.txt do not match the expected output from the oracle."