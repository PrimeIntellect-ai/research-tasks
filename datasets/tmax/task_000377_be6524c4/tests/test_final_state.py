# test_final_state.py
import os
import json
import random
import string
import subprocess
import pytest

def generate_random_input():
    name_length = random.randint(1, 50)
    dataset_name = ''.join(random.choices(string.ascii_letters + string.digits, k=name_length))
    num_rows = random.randint(1, 10_000_000)
    is_public = random.choice([True, False])
    return {
        "dataset_name": dataset_name,
        "num_rows": num_rows,
        "is_public": is_public
    }

def test_fuzz_equivalence():
    agent_script = "/home/user/dataset_encoder.py"
    oracle_program = "/app/oracle_encoder"

    assert os.path.exists(agent_script), f"Agent script {agent_script} does not exist."
    assert os.path.exists(oracle_program), f"Oracle program {oracle_program} does not exist."

    random.seed(42)
    N = 10000

    # Generate all inputs
    inputs = [generate_random_input() for _ in range(N)]

    # To avoid taking too long, we will test a representative sample if 10000 takes too long,
    # but the prompt specifies N=10000. We will run them sequentially.
    # Actually, running 10000 python subprocesses might take ~100 seconds. 
    # Let's run a subset (e.g. 1000) if we want to be safe, but let's stick to 10000 as requested,
    # or just do 1000 to prevent test timeouts. We'll do 1000 to be safe on execution time, 
    # but the prompt says "N = 10000". We will do 10000.

    for i, input_data in enumerate(inputs):
        input_json = json.dumps(input_data)

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_program],
            input=input_json,
            text=True,
            capture_output=True
        )
        oracle_output = oracle_proc.stdout.strip()

        # Run agent
        agent_proc = subprocess.run(
            ["python3", agent_script],
            input=input_json,
            text=True,
            capture_output=True
        )
        agent_output = agent_proc.stdout.strip()

        assert agent_proc.returncode == 0, f"Agent script failed on input: {input_json}\nError: {agent_proc.stderr}"
        assert oracle_output == agent_output, (
            f"Mismatch on input {i+1}/{N}:\n"
            f"Input: {input_json}\n"
            f"Expected (Oracle): {oracle_output}\n"
            f"Got (Agent): {agent_output}"
        )