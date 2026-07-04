# test_final_state.py
import os
import random
import subprocess
import pytest

def test_reconstructed_encoder_exists():
    agent_script = "/home/user/reconstructed_encoder.py"
    assert os.path.exists(agent_script), f"Agent script {agent_script} does not exist."
    assert os.path.isfile(agent_script), f"{agent_script} is not a file."

def test_fuzz_equivalence():
    oracle_path = "/app/malware_encoder"
    agent_script = "/home/user/reconstructed_encoder.py"

    assert os.path.exists(oracle_path), f"Oracle {oracle_path} does not exist."
    assert os.path.exists(agent_script), f"Agent script {agent_script} does not exist."

    random.seed(1337)
    N = 10000
    inputs = [f"{random.uniform(-1000.0, 1000.0):.4f}" for _ in range(N)]
    input_data = "\n".join(inputs) + "\n"

    # Run oracle
    oracle_proc = subprocess.run(
        [oracle_path],
        input=input_data,
        capture_output=True,
        text=True
    )
    assert oracle_proc.returncode == 0, f"Oracle failed with error: {oracle_proc.stderr}"
    oracle_outputs = oracle_proc.stdout.strip().split('\n')

    # Run agent
    agent_proc = subprocess.run(
        ["/usr/bin/python3", agent_script],
        input=input_data,
        capture_output=True,
        text=True
    )
    assert agent_proc.returncode == 0, f"Agent script failed with error: {agent_proc.stderr}"
    agent_outputs = agent_proc.stdout.strip().split('\n')

    assert len(oracle_outputs) == N, f"Oracle output length ({len(oracle_outputs)}) does not match input length ({N})."
    assert len(agent_outputs) == N, f"Agent output length ({len(agent_outputs)}) does not match input length ({N})."

    for i in range(N):
        assert oracle_outputs[i] == agent_outputs[i], (
            f"Mismatch on input {inputs[i]}:\n"
            f"Oracle output: {oracle_outputs[i]}\n"
            f"Agent output:  {agent_outputs[i]}"
        )