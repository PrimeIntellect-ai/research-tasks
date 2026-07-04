# test_final_state.py

import os
import json
import random
import subprocess
import pytest

def test_config_json_fixed():
    config_path = "/app/services/config.json"
    assert os.path.isfile(config_path), f"Config file {config_path} is missing."

    with open(config_path, "r") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Config file {config_path} is not valid JSON.")

    assert "redis_port" in config, "redis_port missing in config.json"
    assert config["redis_port"] == 6379, f"redis_port should be fixed to 6379, but got {config['redis_port']}."

def test_integration_output():
    output_path = "/home/user/integration_output.txt"
    assert os.path.isfile(output_path), f"Integration output file {output_path} is missing. Did you trigger the API?"

    with open(output_path, "r") as f:
        content = f.read()

    assert content.strip() == "20", f"Expected output '20', but got '{content.strip()}' in {output_path}"

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_mol_analyze"
    agent_path = "/app/bin/mol_analyze"

    assert os.path.isfile(agent_path), f"Agent binary {agent_path} is missing."
    assert os.access(agent_path, os.X_OK), f"Agent binary {agent_path} is not executable."

    random.seed(42)
    N_fuzz_iterations = 1000

    for i in range(N_fuzz_iterations):
        V = random.randint(1, 50)
        E = random.randint(0, min(100, V*(V-1)//2))
        edges = []
        possible_edges = [(u,v) for u in range(V) for v in range(u+1, V)]
        selected_edges = random.sample(possible_edges, E)
        for u, v in selected_edges:
            edges.extend([u, v])
        weights = [random.randint(0, 1000) for _ in range(V)]

        input_str = f"{V} {E} " + " ".join(map(str, edges)) + " " + " ".join(map(str, weights))
        input_bytes = input_str.encode('utf-8')

        oracle_proc = subprocess.run([oracle_path], input=input_bytes, capture_output=True)
        agent_proc = subprocess.run([agent_path], input=input_bytes, capture_output=True)

        oracle_out = oracle_proc.stdout.decode('utf-8')
        agent_out = agent_proc.stdout.decode('utf-8')

        if oracle_proc.returncode != 0:
            continue

        assert agent_proc.returncode == 0, f"Agent binary crashed on input: {input_str}"
        assert agent_out == oracle_out, (
            f"Output mismatch on iteration {i}.\n"
            f"Input: {input_str}\n"
            f"Oracle output: {repr(oracle_out)}\n"
            f"Agent output: {repr(agent_out)}"
        )