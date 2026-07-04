# test_final_state.py
import os
import subprocess
import random

def test_fuzz_equivalence():
    agent_exec = "/home/user/process_frame"
    oracle_exec = "/app/oracle_process_frame"

    assert os.path.isfile(agent_exec), f"Agent executable not found at {agent_exec}"
    assert os.access(agent_exec, os.X_OK), f"Agent executable at {agent_exec} is not executable"

    assert os.path.isfile(oracle_exec), f"Oracle executable not found at {oracle_exec}"
    assert os.access(oracle_exec, os.X_OK), f"Oracle executable at {oracle_exec} is not executable"

    random.seed(42)

    for i in range(500):
        # Generate 4096 random bytes
        input_bytes = bytes(random.getrandbits(8) for _ in range(4096))

        # Run agent
        agent_proc = subprocess.run([agent_exec], input=input_bytes, capture_output=True)
        agent_out = agent_proc.stdout

        # Run oracle
        oracle_proc = subprocess.run([oracle_exec], input=input_bytes, capture_output=True)
        oracle_out = oracle_proc.stdout

        assert agent_out == oracle_out, (
            f"Mismatch on fuzz iteration {i}.\n"
            f"Input (first 16 bytes): {input_bytes[:16].hex()}\n"
            f"Oracle output: {oracle_out.decode('utf-8', errors='replace')}\n"
            f"Agent output: {agent_out.decode('utf-8', errors='replace')}"
        )

def test_frame2_stats():
    stats_file = "/home/user/frame2_stats.txt"
    assert os.path.isfile(stats_file), f"Output file not found at {stats_file}"

    with open(stats_file, 'r') as f:
        content = f.read().strip()

    assert content.startswith("Min: ") and "Max: " in content and "Avg: " in content, \
        f"Output file format is incorrect: {content}"

    video_path = "/app/raw_footage.mp4"
    oracle_exec = "/app/oracle_process_frame"
    if os.path.isfile(video_path) and os.path.isfile(oracle_exec):
        ffmpeg_cmd = [
            "ffmpeg", "-i", video_path, "-ss", "00:00:02", "-vframes", "1",
            "-s", "64x64", "-f", "rawvideo", "-pix_fmt", "gray", "-"
        ]
        try:
            ffmpeg_proc = subprocess.run(ffmpeg_cmd, capture_output=True, check=True)
            frame_bytes = ffmpeg_proc.stdout
            if len(frame_bytes) == 4096:
                oracle_proc = subprocess.run([oracle_exec], input=frame_bytes, capture_output=True)
                expected_output = oracle_proc.stdout.decode('utf-8').strip()
                assert content == expected_output, f"Stats file content mismatch. Expected '{expected_output}', got '{content}'"
        except subprocess.CalledProcessError:
            pass