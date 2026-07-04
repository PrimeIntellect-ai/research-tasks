# test_final_state.py
import os
import subprocess
import json
import random
import string
import pytest

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def test_fuzz_equivalence():
    agent_file = "/home/user/loc_render.go"
    oracle_file = "/app/oracle_render"

    assert os.path.isfile(agent_file), f"Agent program {agent_file} does not exist."
    assert os.path.isfile(oracle_file), f"Oracle program {oracle_file} does not exist."

    random.seed(42)

    for i in range(100):
        num_lines = random.randint(0, 20)
        input_data = []
        for _ in range(num_lines):
            record = {
                "screen_id": random.randint(1, 5),
                "key": generate_random_string(random.randint(4, 12)),
                "translation": generate_random_string(random.randint(4, 12))
            }
            input_data.append(json.dumps(record))

        input_str = "\n".join(input_data)
        if input_str:
            input_str += "\n"

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_file],
            input=input_str.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i} with error: {oracle_proc.stderr.decode('utf-8')}"
        oracle_out = oracle_proc.stdout.decode('utf-8')

        # Run agent
        agent_proc = subprocess.run(
            ["go", "run", agent_file],
            input=input_str.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        assert agent_proc.returncode == 0, f"Agent program failed on iteration {i} with error: {agent_proc.stderr.decode('utf-8')}\nInput was:\n{input_str}"
        agent_out = agent_proc.stdout.decode('utf-8')

        assert agent_out == oracle_out, (
            f"Output mismatch on iteration {i}.\n"
            f"Input:\n{input_str}\n"
            f"Expected (Oracle):\n{oracle_out}\n"
            f"Got (Agent):\n{agent_out}"
        )