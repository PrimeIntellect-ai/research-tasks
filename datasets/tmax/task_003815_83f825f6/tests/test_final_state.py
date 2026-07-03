# test_final_state.py

import os
import subprocess
import random
import pytest

def test_frames_extracted():
    frames_dir = "/home/user/frames"
    assert os.path.isdir(frames_dir), f"Directory {frames_dir} does not exist."
    frames = sorted([f for f in os.listdir(frames_dir) if f.endswith('.jpg')])
    assert len(frames) > 0, "No JPEG frames found in the frames directory."
    # Check sequential naming
    for i, frame in enumerate(frames, start=1):
        expected_name = f"{i:04d}.jpg"
        assert frame == expected_name, f"Expected frame name {expected_name}, got {frame}."

def test_raw_sizes_txt():
    raw_sizes_path = "/home/user/raw_sizes.txt"
    frames_dir = "/home/user/frames"
    assert os.path.isfile(raw_sizes_path), f"File {raw_sizes_path} does not exist."

    with open(raw_sizes_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    frames = sorted([f for f in os.listdir(frames_dir) if f.endswith('.jpg')])
    assert len(lines) == len(frames), f"Expected {len(frames)} lines in {raw_sizes_path}, got {len(lines)}."

    for i, frame in enumerate(frames):
        frame_path = os.path.join(frames_dir, frame)
        size = os.path.getsize(frame_path)
        expected_val = "NaN" if size < 5000 else str(size)
        assert lines[i] == expected_val, f"Line {i+1} in {raw_sizes_path} should be '{expected_val}', got '{lines[i]}'."

def test_processed_metrics_csv():
    processed_path = "/home/user/processed_metrics.csv"
    assert os.path.isfile(processed_path), f"File {processed_path} does not exist."

    # We will just verify it exists and has the same number of lines as raw_sizes.txt
    raw_sizes_path = "/home/user/raw_sizes.txt"
    with open(raw_sizes_path, 'r') as f:
        raw_lines = [line.strip() for line in f if line.strip()]

    with open(processed_path, 'r') as f:
        processed_lines = [line.strip() for line in f if line.strip()]

    assert len(processed_lines) == len(raw_lines), f"Expected {len(raw_lines)} lines in {processed_path}, got {len(processed_lines)}."

def test_fuzz_equivalence():
    agent_script = "/home/user/process_stream.sh"
    oracle_script = "/opt/oracle_process_stream.sh"

    assert os.path.isfile(agent_script), f"Agent script {agent_script} does not exist."
    assert os.path.isfile(oracle_script), f"Oracle script {oracle_script} does not exist."

    random.seed(42)
    N = 1000

    for i in range(N):
        num_lines = random.randint(0, 500)
        input_lines = []
        for _ in range(num_lines):
            if random.random() < 0.2:
                input_lines.append("NaN")
            else:
                input_lines.append(str(random.randint(1000, 100000)))

        input_str = "\n".join(input_lines) + ("\n" if input_lines else "")

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_script],
            input=input_str,
            text=True,
            capture_output=True
        )
        oracle_out = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            ["bash", agent_script],
            input=input_str,
            text=True,
            capture_output=True
        )
        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            error_msg = (
                f"Fuzz test failed on iteration {i}.\n"
                f"Input:\n{input_str[:200]}...\n"
                f"Expected Output:\n{oracle_out[:200]}...\n"
                f"Agent Output:\n{agent_out[:200]}...\n"
            )
            pytest.fail(error_msg)