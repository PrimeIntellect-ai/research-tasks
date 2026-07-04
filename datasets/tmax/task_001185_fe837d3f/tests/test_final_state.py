# test_final_state.py

import os
import random
import subprocess
import pytest

def test_analyze_fuzz_equivalence():
    agent_exe = "/home/user/analyze"
    oracle_exe = "/app/oracle_analyze"

    assert os.path.isfile(agent_exe), f"Agent executable {agent_exe} not found."
    assert os.access(agent_exe, os.X_OK), f"Agent {agent_exe} is not executable."

    random.seed(42)

    # Run 50 fuzz tests
    for i in range(50):
        N = random.randint(10, 500)
        input_data = " ".join(str(random.uniform(-1000.0, 1000.0)) for _ in range(N))

        agent_proc = subprocess.run([agent_exe], input=input_data, text=True, capture_output=True)
        oracle_proc = subprocess.run([oracle_exe], input=input_data, text=True, capture_output=True)

        assert agent_proc.returncode == 0, f"Agent crashed on input {i}: {agent_proc.stderr}"
        assert oracle_proc.returncode == 0, f"Oracle crashed on input {i}"

        agent_out = agent_proc.stdout.strip()
        oracle_out = oracle_proc.stdout.strip()

        assert agent_out == oracle_out, (
            f"Mismatch on fuzz test {i} (N={N}).\n"
            f"Input start: {input_data[:50]}...\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}"
        )

def test_frame_means_and_video_analysis():
    frame_means_path = "/home/user/frame_means.txt"
    video_analysis_path = "/home/user/video_analysis.txt"
    video_path = "/app/experiment.mp4"
    oracle_exe = "/app/oracle_analyze"

    assert os.path.isfile(frame_means_path), f"{frame_means_path} not found."
    assert os.path.isfile(video_analysis_path), f"{video_analysis_path} not found."

    # Recompute frame means using ffmpeg to extract raw bytes
    cmd = [
        "ffmpeg", "-i", video_path, "-f", "rawvideo", "-pix_fmt", "gray", "-"
    ]
    proc = subprocess.run(cmd, capture_output=True, check=True)
    raw_bytes = proc.stdout

    frame_size = 64 * 64
    expected_means = []
    for i in range(0, len(raw_bytes), frame_size):
        frame = raw_bytes[i:i+frame_size]
        if len(frame) == frame_size:
            mean_val = sum(frame) / frame_size
            expected_means.append(mean_val)

    with open(frame_means_path, "r") as f:
        agent_means_str = f.read().split()

    assert len(agent_means_str) == len(expected_means), (
        f"Number of frame means does not match. "
        f"Expected {len(expected_means)}, got {len(agent_means_str)}."
    )

    for i, (a_str, e_val) in enumerate(zip(agent_means_str, expected_means)):
        try:
            a_val = float(a_str)
        except ValueError:
            pytest.fail(f"Invalid float value in frame means at index {i}: {a_str}")
        assert abs(a_val - e_val) < 0.5, f"Frame {i} mean mismatch: expected ~{e_val}, got {a_val}"

    # Check video_analysis.txt by running the oracle on the generated frame means
    with open(frame_means_path, "r") as f:
        frame_means_content = f.read()

    oracle_proc = subprocess.run([oracle_exe], input=frame_means_content, text=True, capture_output=True)
    expected_analysis = oracle_proc.stdout.strip()

    with open(video_analysis_path, "r") as f:
        agent_analysis = f.read().strip()

    assert agent_analysis == expected_analysis, (
        f"Video analysis output mismatch.\n"
        f"Expected: {expected_analysis}\n"
        f"Got: {agent_analysis}"
    )