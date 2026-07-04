# test_final_state.py
import os
import json
import random
import subprocess
from pymongo import MongoClient

def test_database_content():
    """Verify that the MongoDB database is correctly populated from the video."""
    video_path = "/app/experiment.mp4"
    assert os.path.exists(video_path), f"Video file {video_path} is missing."

    # Extract frames using the exact ffmpeg command specified
    cmd = [
        "ffmpeg", "-i", video_path, 
        "-f", "image2pipe", 
        "-pix_fmt", "gray", 
        "-vcodec", "rawvideo", 
        "-"
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    assert proc.returncode == 0, "Failed to run ffmpeg to extract video frames."

    video_data = proc.stdout
    frame_size = 320 * 240

    expected_frames = []
    num_frames = len(video_data) // frame_size
    for i in range(num_frames):
        frame_bytes = video_data[i * frame_size : (i + 1) * frame_size]
        # Count pixels strictly greater than 200
        bright_pixels = sum(1 for p in frame_bytes if p > 200)
        expected_frames.append({"frame": i, "bright_pixels": bright_pixels})

    try:
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
    except Exception as e:
        assert False, f"Could not connect to MongoDB: {e}"

    db = client["research"]
    collection = db["frames"]

    actual_frames = list(collection.find({}, {"_id": 0, "frame": 1, "bright_pixels": 1}).sort("frame", 1))

    assert len(actual_frames) == len(expected_frames), \
        f"Database has {len(actual_frames)} frames, expected {len(expected_frames)}."

    for actual, expected in zip(actual_frames, expected_frames):
        assert actual.get("frame") == expected["frame"], \
            f"Frame index mismatch: got {actual.get('frame')}, expected {expected['frame']}."
        assert actual.get("bright_pixels") == expected["bright_pixels"], \
            f"Bright pixels mismatch at frame {expected['frame']}: got {actual.get('bright_pixels')}, expected {expected['bright_pixels']}."

def test_fuzz_equivalence():
    """Fuzz test the agent's C program against the oracle."""
    oracle_path = "/app/oracle_query"
    agent_path = "/home/user/query_frames"

    assert os.path.isfile(oracle_path), f"Oracle binary {oracle_path} is missing."
    assert os.path.isfile(agent_path), f"Agent binary {agent_path} is missing. Did you compile the C program?"

    random.seed(42)
    fuzz_n_inputs = 50

    for i in range(fuzz_n_inputs):
        min_frame = random.randint(0, 300)
        max_frame = random.randint(0, 300)
        min_bright = random.randint(0, 76800)

        args = [str(min_frame), str(max_frame), str(min_bright)]

        proc_oracle = subprocess.run([oracle_path] + args, capture_output=True, text=True)
        proc_agent = subprocess.run([agent_path] + args, capture_output=True, text=True)

        assert proc_agent.returncode == 0, \
            f"Agent program exited with code {proc_agent.returncode} on args {args}. Stderr: {proc_agent.stderr}"

        try:
            oracle_json = json.loads(proc_oracle.stdout)
        except json.JSONDecodeError:
            # Fallback if oracle output is not strictly JSON (should not happen based on spec)
            oracle_json = proc_oracle.stdout.strip()

        try:
            agent_json = json.loads(proc_agent.stdout)
        except json.JSONDecodeError:
            assert False, f"Agent output is not valid JSON on args {args}. Output: {proc_agent.stdout}"

        assert agent_json == oracle_json, \
            f"Output mismatch on args {args}.\nExpected (Oracle): {oracle_json}\nGot (Agent): {agent_json}"