# test_final_state.py

import os
import json
import random
import subprocess
import tempfile
import pytest

def test_fuzz_equivalence():
    oracle_path = "/app/oracle.py"
    agent_path = "/home/user/transform.py"

    assert os.path.isfile(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent script missing at {agent_path}"

    random.seed(42)
    N = 100
    for i in range(N):
        L = random.randint(10, 100)
        data = [[random.uniform(-500.0, 500.0), random.uniform(-500.0, 500.0)] for _ in range(L)]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f_in:
            json.dump(data, f_in)
            in_path = f_in.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f_oracle:
            oracle_out_path = f_oracle.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f_agent:
            agent_out_path = f_agent.name

        try:
            subprocess.run(["python3", oracle_path, in_path, oracle_out_path], check=True, capture_output=True)
            res = subprocess.run(["python3", agent_path, in_path, agent_out_path], capture_output=True, text=True)
            assert res.returncode == 0, f"Agent script failed on fuzz input {i}:\n{res.stderr}"

            with open(oracle_out_path, 'r') as f:
                oracle_out = f.read()
            with open(agent_out_path, 'r') as f:
                agent_out = f.read()

            assert oracle_out == agent_out, f"Mismatch on fuzz input {i}:\nInput: {data}\nOracle: {oracle_out}\nAgent: {agent_out}"
        finally:
            if os.path.exists(in_path): os.remove(in_path)
            if os.path.exists(oracle_out_path): os.remove(oracle_out_path)
            if os.path.exists(agent_out_path): os.remove(agent_out_path)

def test_trajectory_json():
    traj_path = "/home/user/trajectory.json"
    assert os.path.isfile(traj_path), f"Missing {traj_path}"
    with open(traj_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {traj_path} is not valid JSON")

    assert isinstance(data, list), "Trajectory should be a JSON array"
    assert len(data) == 300, f"Expected 300 frames in trajectory.json, got {len(data)}"
    for point in data:
        assert isinstance(point, list) and len(point) == 2, "Each point must be a 2-element array"
        assert isinstance(point[0], (int, float)) and isinstance(point[1], (int, float)), "Coordinates must be numbers"

def test_video_tokens():
    tokens_path = "/home/user/video_tokens.txt"
    traj_path = "/home/user/trajectory.json"
    oracle_path = "/app/oracle.py"

    assert os.path.isfile(tokens_path), f"Missing {tokens_path}"
    assert os.path.isfile(traj_path), f"Missing {traj_path}"

    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f_oracle:
        oracle_out_path = f_oracle.name

    try:
        subprocess.run(["python3", oracle_path, traj_path, oracle_out_path], check=True)
        with open(oracle_out_path, 'r') as f:
            expected_tokens = f.read()
        with open(tokens_path, 'r') as f:
            actual_tokens = f.read()
        assert actual_tokens == expected_tokens, "video_tokens.txt does not match oracle output for trajectory.json"
    finally:
        if os.path.exists(oracle_out_path): os.remove(oracle_out_path)

def test_centered_plot():
    plot_path = "/home/user/centered_plot.png"
    assert os.path.isfile(plot_path), f"Missing {plot_path}"
    assert os.path.getsize(plot_path) > 0, "Plot file is empty"

    with open(plot_path, 'rb') as f:
        header = f.read(8)
    assert header == b'\x89PNG\r\n\x1a\n', "Plot file is not a valid PNG"