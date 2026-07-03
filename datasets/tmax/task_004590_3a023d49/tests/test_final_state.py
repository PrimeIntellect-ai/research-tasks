# test_final_state.py

import os
import json
import random
import string
import subprocess
import pytest

def generate_random_input(seed):
    random.seed(seed)
    existing_nodes = ["ROOT", "DB_1", "DB_2", "Collection_A", "Collection_B", "Collection_C"]
    num_new_nodes = random.randint(1, 5)
    new_nodes = [
        ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(4, 12)))
        for _ in range(num_new_nodes)
    ]

    edges = []
    current_existing = list(existing_nodes)
    for new_node in new_nodes:
        source = random.choice(current_existing)
        edges.append({"source": source, "target": new_node})
        current_existing.append(new_node)

    # Add some extra random edges between existing nodes just in case
    for _ in range(random.randint(0, 3)):
        src = random.choice(current_existing)
        dst = random.choice(current_existing)
        if src != dst:
            edges.append({"source": src, "target": dst})

    return json.dumps(edges)

def run_script(script_path, input_data):
    if script_path.endswith('.py'):
        cmd = ["python3", script_path]
    else:
        cmd = [script_path]

    result = subprocess.run(
        cmd,
        input=input_data,
        text=True,
        capture_output=True
    )
    return result

def test_agent_script_exists():
    assert os.path.isfile('/home/user/etl_graph.py'), "/home/user/etl_graph.py does not exist"

def test_fuzz_equivalence():
    agent_script = '/home/user/etl_graph.py'
    oracle_script = '/app/oracle_etl_graph.py'

    assert os.path.isfile(agent_script), f"Agent script {agent_script} not found."
    assert os.path.isfile(oracle_script), f"Oracle script {oracle_script} not found."

    N = 100
    for i in range(N):
        input_data = generate_random_input(seed=42 + i)

        agent_result = run_script(agent_script, input_data)
        oracle_result = run_script(oracle_script, input_data)

        assert agent_result.returncode == 0, f"Agent script failed on input: {input_data}\nStderr: {agent_result.stderr}"
        assert oracle_result.returncode == 0, f"Oracle script failed on input: {input_data}\nStderr: {oracle_result.stderr}"

        try:
            agent_json = json.loads(agent_result.stdout)
        except json.JSONDecodeError:
            pytest.fail(f"Agent output is not valid JSON. Output: {agent_result.stdout}\nInput: {input_data}")

        try:
            oracle_json = json.loads(oracle_result.stdout)
        except json.JSONDecodeError:
            pytest.fail(f"Oracle output is not valid JSON. Output: {oracle_result.stdout}\nInput: {input_data}")

        assert agent_json == oracle_json, (
            f"Mismatch on input {i}.\n"
            f"Input: {input_data}\n"
            f"Oracle output: {oracle_json}\n"
            f"Agent output: {agent_json}"
        )