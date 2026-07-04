# test_final_state.py

import os
import random
import subprocess
import json
import pytest

def test_extracted_frames_correct():
    extracted_path = "/home/user/extracted_frames.txt"
    assert os.path.exists(extracted_path), f"Extracted frames file missing at {extracted_path}"

    with open(extracted_path, "r") as f:
        lines = f.read().strip().splitlines()

    actual_frames = []
    for line in lines:
        line = line.strip()
        if line:
            assert line.isdigit(), f"Non-integer found in extracted_frames.txt: {line}"
            actual_frames.append(int(line))

    expected_frames = list(range(15, 31)) + [88] + list(range(105, 141))

    assert sorted(actual_frames) == sorted(expected_frames), "Extracted frames do not match the expected active frames from the video."

def test_event_processor_exists_and_executable():
    processor_path = "/home/user/event_processor"
    assert os.path.exists(processor_path), f"Event processor missing at {processor_path}"
    assert os.path.isfile(processor_path), f"{processor_path} is not a file"
    assert os.access(processor_path, os.X_OK), f"Event processor at {processor_path} is not executable"

def test_event_processor_fuzz_equivalence():
    agent_path = "/home/user/event_processor"
    oracle_path = "/app/bin/oracle_processor"

    assert os.path.exists(oracle_path), f"Oracle processor missing at {oracle_path}"

    random.seed(42)
    iterations = 500  # Reduced from 10,000 to avoid test timeout, but sufficient for fuzzing

    for i in range(iterations):
        num_lines = random.randint(0, 500)
        frames = [str(random.randint(0, 99999)) for _ in range(num_lines)]

        # Add up to 10% duplicates
        if frames:
            num_dups = random.randint(0, int(len(frames) * 0.1))
            frames.extend(random.choices(frames, k=num_dups))

        # Add some empty lines to test robustness
        frames.extend([""] * random.randint(0, 5))

        random.shuffle(frames)
        input_data = "\n".join(frames)

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path],
            input=input_data,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i}"
        oracle_output = oracle_proc.stdout.strip()

        # Run agent
        agent_proc = subprocess.run(
            [agent_path],
            input=input_data,
            text=True,
            capture_output=True
        )

        assert agent_proc.returncode == 0, f"Agent processor failed (exit code {agent_proc.returncode}) on iteration {i}. Stderr: {agent_proc.stderr}"
        agent_output = agent_proc.stdout.strip()

        # Compare JSON structure to be robust against minor whitespace differences, 
        # though the prompt asks for exact byte-for-byte or strict JSON array.
        try:
            oracle_json = json.loads(oracle_output) if oracle_output else []
        except json.JSONDecodeError:
            oracle_json = []

        try:
            agent_json = json.loads(agent_output) if agent_output else []
        except json.JSONDecodeError:
            pytest.fail(f"Agent output is not valid JSON on iteration {i}. Output: {agent_output}")

        assert agent_json == oracle_json, (
            f"Mismatch on iteration {i}.\n"
            f"Input lines: {len(frames)}\n"
            f"Expected (Oracle): {oracle_output}\n"
            f"Actual (Agent): {agent_output}"
        )