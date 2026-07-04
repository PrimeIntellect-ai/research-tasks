# test_final_state.py

import os
import json
import random
import subprocess
import pytest

def test_agent_executable_exists():
    path = "/home/user/bin/infer"
    assert os.path.isfile(path), f"Agent executable missing: {path}"
    assert os.access(path, os.X_OK), f"Agent executable not executable: {path}"

def test_video_scene_changes_json_exists_and_valid():
    path = "/home/user/video_scene_changes.json"
    assert os.path.isfile(path), f"Output JSON missing: {path}"
    with open(path, "r") as f:
        try:
            data = json.load(f)
            assert isinstance(data, list), "Output must be a JSON array"
            for item in data:
                assert isinstance(item, int), f"Expected integer indices, got {type(item)}"
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON")

def test_fuzz_equivalence():
    oracle_path = "/app/bin/oracle_infer"
    agent_path = "/home/user/bin/infer"

    assert os.path.isfile(oracle_path), f"Oracle missing: {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle not executable: {oracle_path}"

    random.seed(42)
    N = 500

    for i in range(N):
        outer_length = random.randint(10, 100)
        input_data = []
        for _ in range(outer_length):
            row = [random.uniform(0.0, 255.0) for _ in range(16)]
            input_data.append(row)

        input_json = json.dumps(input_data)

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path],
            input=input_json,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input {i}. Stderr: {oracle_proc.stderr}"

        # Run agent
        agent_proc = subprocess.run(
            [agent_path],
            input=input_json,
            text=True,
            capture_output=True
        )
        assert agent_proc.returncode == 0, f"Agent failed on input {i}. Stderr: {agent_proc.stderr}"

        try:
            oracle_out = json.loads(oracle_proc.stdout)
        except json.JSONDecodeError:
            pytest.fail(f"Oracle output invalid JSON on input {i}: {oracle_proc.stdout}")

        try:
            agent_out = json.loads(agent_proc.stdout)
        except json.JSONDecodeError:
            pytest.fail(f"Agent output invalid JSON on input {i}: {agent_proc.stdout}")

        assert agent_out == oracle_out, (
            f"Mismatch on input {i}.\n"
            f"Input: {input_json}\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output: {agent_out}"
        )