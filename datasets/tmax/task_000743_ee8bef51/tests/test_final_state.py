# test_final_state.py

import os
import json
import random
import subprocess
import pytest

def test_frame_analyzer_fuzz_equivalence():
    oracle_path = "/app/oracle_analyzer"
    agent_path = "/home/user/analyzer/frame_analyzer"

    assert os.path.isfile(agent_path), f"Agent binary not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable"

    random.seed(42)
    for i in range(500):
        length = random.randint(3, 30000)
        input_data = bytearray(random.getrandbits(8) for _ in range(length))

        oracle_proc = subprocess.run([oracle_path], input=input_data, capture_output=True)
        agent_proc = subprocess.run([agent_path], input=input_data, capture_output=True)

        assert oracle_proc.returncode == 0, f"Oracle failed on input of length {length}"
        assert agent_proc.returncode == 0, f"Agent failed on input of length {length}"

        oracle_out = oracle_proc.stdout.decode('utf-8', errors='replace').strip()
        agent_out = agent_proc.stdout.decode('utf-8', errors='replace').strip()

        assert agent_out == oracle_out, f"Mismatch on input {i} (length {length}). Expected: {oracle_out}, Got: {agent_out}"

def test_highest_frame_json():
    json_path = "/home/user/highest_frame.json"
    assert os.path.isfile(json_path), f"Expected result file not found at {json_path}"

    with open(json_path, "r") as f:
        try:
            result = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("highest_frame.json is not valid JSON")

    assert "frame" in result, "Result JSON missing 'frame' key"
    assert "score" in result, "Result JSON missing 'score' key"

    # Compute the expected highest frame using the oracle
    oracle_path = "/app/oracle_analyzer"
    video_path = "/app/terminal_e2e.mp4"

    highest_frame = -1
    highest_score = -1

    for frame_idx in range(101):
        # Extract frame
        ffmpeg_cmd = [
            "ffmpeg", "-y", "-i", video_path,
            "-vf", f"select=eq(n\\,{frame_idx})",
            "-vframes", "1",
            "-f", "rawvideo",
            "-pix_fmt", "rgb24",
            "-"
        ]
        ffmpeg_proc = subprocess.run(ffmpeg_cmd, capture_output=True)
        if ffmpeg_proc.returncode != 0:
            continue

        frame_data = ffmpeg_proc.stdout
        if not frame_data:
            continue

        oracle_proc = subprocess.run([oracle_path], input=frame_data, capture_output=True)
        if oracle_proc.returncode == 0:
            try:
                score = int(oracle_proc.stdout.decode('utf-8').strip())
                if score > highest_score:
                    highest_score = score
                    highest_frame = frame_idx
            except ValueError:
                pass

    assert result["frame"] == highest_frame, f"Expected highest frame to be {highest_frame}, but got {result['frame']}"
    assert result["score"] == highest_score, f"Expected highest score to be {highest_score}, but got {result['score']}"