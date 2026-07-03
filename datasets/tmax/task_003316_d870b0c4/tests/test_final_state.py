# test_final_state.py

import os
import json
import random
import string
import subprocess
import pytest

def test_video_graph_result():
    result_path = "/home/user/video_graph_result.json"
    assert os.path.exists(result_path), f"File {result_path} is missing. Did you save the final JSON?"

    with open(result_path, 'r') as f:
        content = f.read().strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"File {result_path} does not contain valid JSON. Content: {content}")

    expected = ["AuthModule", "InitDB", "StartServer", "AcceptRequests", "ProcessData"]
    assert data == expected, f"Expected JSON array {expected}, but got {data}"

def test_resolver_binary_exists():
    binary_path = "/home/user/resolver"
    assert os.path.isfile(binary_path), f"Binary {binary_path} is missing. Did you compile your C code?"
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def generate_random_graph(num_edges, force_cycle):
    charset = string.ascii_letters + string.digits
    def random_node():
        length = random.randint(1, 15)
        return "".join(random.choices(charset, k=length))

    num_nodes = max(2, num_edges)
    nodes = [random_node() for _ in range(num_nodes)]

    edges = []
    if force_cycle and num_edges >= 2:
        cycle_len = random.randint(2, min(num_edges, len(nodes)))
        cycle_nodes = random.sample(nodes, cycle_len)
        for i in range(cycle_len):
            edges.append(f"{cycle_nodes[i]}:{cycle_nodes[(i+1)%cycle_len]}")

        for _ in range(num_edges - cycle_len):
            u = random.choice(nodes)
            v = random.choice(nodes)
            edges.append(f"{u}:{v}")
    else:
        for _ in range(num_edges):
            u_idx = random.randint(0, len(nodes) - 2)
            v_idx = random.randint(u_idx + 1, len(nodes) - 1)
            edges.append(f"{nodes[u_idx]}:{nodes[v_idx]}")

    # Shuffle edges so they are not strictly ordered in input
    random.shuffle(edges)
    return "\n".join(edges) + ("\n" if edges else "")

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_resolver"
    agent_path = "/home/user/resolver"

    assert os.path.isfile(oracle_path), f"Oracle {oracle_path} missing."
    assert os.path.isfile(agent_path), f"Agent binary {agent_path} missing."

    random.seed(1337)
    N = 1000

    for i in range(N):
        num_edges = random.randint(0, 150)
        force_cycle = random.random() < 0.3

        graph_input = generate_random_graph(num_edges, force_cycle)

        oracle_proc = subprocess.run([oracle_path], input=graph_input, text=True, capture_output=True)
        agent_proc = subprocess.run([agent_path], input=graph_input, text=True, capture_output=True)

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        if oracle_out != agent_out:
            pytest.fail(
                f"Fuzz test failed on iteration {i}.\n"
                f"Input Graph:\n{graph_input}\n"
                f"Oracle Output:\n{oracle_out}\n"
                f"Agent Output:\n{agent_out}\n"
                f"Agent Stderr:\n{agent_proc.stderr.strip()}"
            )