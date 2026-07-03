# test_final_state.py
import os
import random
import subprocess
import tempfile
import pytest

ORACLE_PATH = "/app/oracle_video_etl.py"
AGENT_PATH = "/home/user/video_etl.py"
NUM_TESTS = 10

def generate_synthetic_video(duration, output_path):
    cmd = [
        "ffmpeg", "-y", "-f", "lavfi",
        f"i=testsrc=duration={duration}:size=320x240:rate=24",
        "-c:v", "libx264", output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def run_script(script_path, video_path):
    cmd = ["python3", script_path, video_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout, result.stderr

def test_fuzz_equivalence():
    assert os.path.isfile(AGENT_PATH), f"Agent script not found at {AGENT_PATH}"
    assert os.path.isfile(ORACLE_PATH), f"Oracle script not found at {ORACLE_PATH}"

    random.seed(42)
    durations = [random.randint(5, 30) for _ in range(NUM_TESTS)]

    with tempfile.TemporaryDirectory() as tmpdir:
        for i, duration in enumerate(durations):
            video_path = os.path.join(tmpdir, f"test_{i}.mp4")
            generate_synthetic_video(duration, video_path)

            oracle_out, _ = run_script(ORACLE_PATH, video_path)
            agent_out, agent_err = run_script(AGENT_PATH, video_path)

            assert agent_out == oracle_out, (
                f"Mismatch on video duration {duration}s.\n"
                f"Oracle output:\n{oracle_out}\n"
                f"Agent output:\n{agent_out}\n"
                f"Agent stderr:\n{agent_err}"
            )