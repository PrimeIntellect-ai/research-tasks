# test_final_state.py

import os
import subprocess
import random
import pytest

def test_video_sum_correct():
    path = "/home/user/video_sum.txt"
    assert os.path.isfile(path), f"Missing {path}"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "582390", f"Expected sum 582390, got {content}"

def test_frame_decoder_fuzz_equivalence():
    agent_bin = "/home/user/frame_decoder"
    oracle_bin = "/app/oracle_decoder"

    assert os.path.isfile(agent_bin), f"Agent binary not found at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary {agent_bin} is not executable"

    assert os.path.isfile(oracle_bin), f"Oracle binary not found at {oracle_bin}"
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary {oracle_bin} is not executable"

    random.seed(42)
    n_iterations = 10000
    size = 4096

    magic = b'\xde\xad\xbe\xef'

    for i in range(n_iterations):
        if i % 10 == 0:
            # Valid frame
            data = bytearray(random.getrandbits(8) for _ in range(size))
            data[0:4] = magic
            input_data = bytes(data)
        else:
            # Random frame
            input_data = bytes(random.getrandbits(8) for _ in range(size))

        # Run oracle
        proc_oracle = subprocess.run(
            [oracle_bin],
            input=input_data,
            capture_output=True
        )

        # Run agent
        proc_agent = subprocess.run(
            [agent_bin],
            input=input_data,
            capture_output=True
        )

        assert proc_oracle.returncode == proc_agent.returncode, f"Return code mismatch on iteration {i}. Oracle: {proc_oracle.returncode}, Agent: {proc_agent.returncode}"
        assert proc_oracle.stdout == proc_agent.stdout, f"Stdout mismatch on iteration {i}. Oracle: {proc_oracle.stdout!r}, Agent: {proc_agent.stdout!r}"