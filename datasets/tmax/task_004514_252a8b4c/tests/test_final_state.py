# test_final_state.py

import os
import json
import random
import string
import subprocess
import pytest

def generate_fuzz_input(n=1000):
    random.seed(42)
    lines = []

    # Edge cases
    lines.append({"id": "empty123", "text": ""})
    lines.append({"id": "punct123", "text": "!@#$%^&*()"})
    lines.append({"id": "long1234", "text": "a b c d e f g h i j k l m n o p"})
    lines.append({"id": "repeat12", "text": "repeat this text"})
    lines.append({"id": "repeat34", "text": "repeat this text"})

    # Random cases
    for _ in range(n - 5):
        id_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        text_len = random.randint(10, 200)
        text_chars = []
        for _ in range(text_len):
            if random.random() < 0.8:
                text_chars.append(random.choice(string.printable))
            else:
                # Include some non-ascii unicode characters
                text_chars.append(chr(random.randint(0x00A0, 0x02AF)))
        text_str = ''.join(text_chars)
        lines.append({"id": id_str, "text": text_str})

    return "\n".join(json.dumps(obj) for obj in lines) + "\n"

def test_fuzz_equivalence():
    agent_bin = "/home/user/rust_worker/target/release/process_data"
    oracle_bin = "/app/oracle_processor"

    assert os.path.exists(agent_bin), f"Agent binary not found at {agent_bin}. Did you build the release binary?"
    assert os.path.exists(oracle_bin), f"Oracle binary not found at {oracle_bin}"

    input_data = generate_fuzz_input(1000)

    agent_proc = subprocess.run([agent_bin], input=input_data, text=True, capture_output=True)
    oracle_proc = subprocess.run([oracle_bin], input=input_data, text=True, capture_output=True)

    assert agent_proc.returncode == 0, f"Agent binary failed with return code {agent_proc.returncode}.\nStderr: {agent_proc.stderr}"
    assert oracle_proc.returncode == 0, f"Oracle binary failed with return code {oracle_proc.returncode}.\nStderr: {oracle_proc.stderr}"

    agent_lines = agent_proc.stdout.strip().split('\n')
    oracle_lines = oracle_proc.stdout.strip().split('\n')

    assert len(agent_lines) == len(oracle_lines), f"Output line count mismatch. Oracle produced {len(oracle_lines)} lines, Agent produced {len(agent_lines)} lines."

    input_lines = input_data.strip().split('\n')

    for i, (al, ol) in enumerate(zip(agent_lines, oracle_lines)):
        try:
            aj = json.loads(al)
        except json.JSONDecodeError:
            pytest.fail(f"Agent output is not valid JSON at line {i+1}.\nInput: {input_lines[i]}\nAgent output: {al}")

        try:
            oj = json.loads(ol)
        except json.JSONDecodeError:
            pytest.fail(f"Oracle output is not valid JSON at line {i+1}. Oracle output: {ol}")

        assert aj == oj, (
            f"Mismatch at line {i+1}.\n"
            f"Input: {input_lines[i]}\n"
            f"Oracle Expected: {ol}\n"
            f"Agent Produced:  {al}"
        )